#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculation logic for Gen 1 Pokemon battle decisions.
Separated from state management to keep concerns distinct.

This module handles:
- Damage calculations (with stat mods, status effects, screens)
- Outspeed probability calculations
- Status move value calculations
- NPW score predictions via KNN
"""
import math
import pandas as pd
from os import path
from sklearn.neighbors import KNeighborsRegressor
from poke_env.battle import Pokemon, Move, Battle, Status, SideCondition, Effect

from general_poke_data import gen1_mons_dict, gen1_moves_dict, type_effectiveness_dict


class Gen1BattleThinker:
    """Handles all battle calculations and predictions."""

    # Types that use Special stat in Gen 1
    SPECIAL_TYPES = frozenset(['Grass', 'Psychic', 'Ice', 'Water', 'Dragon', 'Fire', 'Electric', 'Dark'])

    def __init__(self, username: str, read_csv: str = './data/battle_records_combined.csv'):
        self._username = username
        self._read_csv = read_csv
        self._load_training_data()

    def _load_training_data(self):
        """Load KNN training data from CSV if available."""
        if path.exists(self._read_csv):
            self._training_data = pd.read_csv(self._read_csv, index_col=False)
            n_neighbors = max(1, math.floor(math.sqrt(self._training_data.shape[0])))
            self._knner = KNeighborsRegressor(n_neighbors=n_neighbors).fit(
                self._training_data[['self_hp', 'opp_hp', 'outspeed_prob',
                                     'is_status_move', 'exp_damage_done',
                                     'exp_damage_received']],
                self._training_data.actual_npw_score
            )
            self._knnpred = lambda df: self._knner.predict(df)[0]
            print(f"Loaded {len(self._training_data)} training records from {self._read_csv}")
        else:
            self._training_data = pd.DataFrame()
            self._knnpred = lambda df: 0
            print("No training data found, starting fresh")

    def get_action_metrics(self, battle: Battle, action: tuple) -> dict:
        """
        Calculate all metrics for a given action.

        Args:
            battle: Current battle state from poke-env
            action: Tuple of (action_type, action_obj) where action_type is 'move' or 'switch'

        Returns:
            Dictionary with all calculated metrics for this action
        """
        action_type, action_obj = action
        m = {}

        if action_type == 'move':
            m['is_switch'] = False
            m['action_name'] = action_obj.id
            m['battle_order'] = ('move', action_obj)
        else:
            m['is_switch'] = True
            m['action_name'] = action_obj.species
            m['battle_order'] = ('switch', action_obj)

        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon

        m['self_hp'] = my_mon.current_hp_fraction if my_mon else 1.0
        m['opp_hp'] = opp_mon.current_hp_fraction if opp_mon else 1.0
        m['outspeed_prob'] = self._get_outspeed_prob(battle, action)
        m['is_status_move'] = self._get_status_move_value(battle, action)
        m['exp_damage_done'] = self._get_damage_done(battle, action)
        m['exp_damage_received'] = self._get_damage_received(battle, action)
        m['predicted_npw_score'] = self._get_predicted_npw_score(m)

        return m

    def _get_predicted_npw_score(self, metrics: dict) -> float:
        """Predict NPW score using KNN model."""
        metrics_df = pd.DataFrame({
            'self_hp': [metrics['self_hp']],
            'opp_hp': [metrics['opp_hp']],
            'outspeed_prob': [metrics['outspeed_prob']],
            'is_status_move': [metrics['is_status_move']],
            'exp_damage_done': [metrics['exp_damage_done']],
            'exp_damage_received': [metrics['exp_damage_received']]
        })
        return self._knnpred(metrics_df)

    def _get_outspeed_prob(self, battle: Battle, action: tuple) -> float:
        """
        Calculate probability of outspeeding opponent.

        Accounts for:
        - Switch actions (always go first)
        - Priority moves (Quick Attack)
        - Counter (always goes last)
        - Speed stats with stat modifiers
        - Paralysis speed reduction
        - Opponent's potential Counter/Quick Attack usage
        """
        action_type, action_obj = action

        if action_type == 'switch':
            return 1.0

        move = action_obj
        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon

        if not my_mon or not opp_mon:
            return 0.5

        # Priority move handling
        try:
            move_priority = move.priority
        except (KeyError, AttributeError):
            move_priority = 0

        if move.id == 'quickattack' or move_priority > 0:
            return 1.0
        if move.id == 'counter':
            return 0.0

        # Calculate my speed with stat mods and paralysis
        my_speed = self._get_stat_with_mods(my_mon, 'spe', is_own_pokemon=True)
        if my_mon.status == Status.PAR:
            my_speed *= 0.25

        # Calculate opponent speed with stat mods and paralysis
        opp_speed = self._get_opponent_speed(opp_mon)

        # Check opponent's known moves for Counter/Quick Attack
        opp_has_counter = self._opponent_has_move(opp_mon, 'counter')
        opp_has_quick_attack = self._opponent_has_move(opp_mon, 'quickattack')

        if opp_speed > my_speed:
            # Opponent is faster
            if opp_has_counter:
                return 0.25  # They might use Counter, giving us a chance
            return 0.0
        elif opp_speed == my_speed:
            # Speed tie
            if opp_has_counter and opp_has_quick_attack:
                return 0.5
            elif opp_has_counter:
                return 0.375
            elif opp_has_quick_attack:
                return 0.625
            return 0.5
        else:
            # We are faster
            if opp_has_quick_attack:
                return 0.75  # They might outspeed with Quick Attack
            return 1.0

    def _get_status_move_value(self, battle: Battle, action: tuple) -> float:
        """
        Calculate value of status move based on accuracy and effect chance.

        Accounts for:
        - Pure status moves (Sleep Powder, Thunder Wave, etc.)
        - Moves with secondary status effects (Body Slam paralysis chance)
        - Accuracy/evasion stat modifiers
        """
        action_type, action_obj = action

        if action_type == 'switch':
            return 0.0

        move = action_obj
        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon

        # Handle special moves like "recharge" that don't have normal properties
        try:
            move_category = move.category.name
        except (KeyError, AttributeError):
            return 0.0

        move_name = self._normalize_move_name(move.id)
        move_data = gen1_moves_dict.get(move_name, {})

        if move_category == 'STATUS':
            # Pure status move
            if 'accuracy' in move_data:
                base_acc = move_data['accuracy'] / 100
            else:
                base_acc = 1.0

            # Apply accuracy/evasion modifiers
            acc_mod = self._get_accuracy_modifier(my_mon, opp_mon)
            return min(base_acc * acc_mod, 1.0)

        elif 'statusperc' in move_data:
            # Damaging move with status side effect
            if 'accuracy' in move_data:
                base_acc = move_data['accuracy'] / 100
            else:
                base_acc = 1.0
            status_chance = move_data['statusperc'] / 100
            acc_mod = self._get_accuracy_modifier(my_mon, opp_mon)
            return min(base_acc * acc_mod * status_chance, 1.0)

        return 0.0

    def _get_damage_done(self, battle: Battle, action: tuple) -> float:
        """
        Calculate expected damage dealt as fraction of opponent's max HP.

        Accounts for:
        - Status moves (0 damage)
        - Fixed damage moves (Seismic Toss, Night Shade, Dragon Rage)
        - Full damage formula with stat modifiers
        - STAB bonus
        - Type effectiveness
        - Accuracy and accuracy/evasion modifiers
        - Paralysis damage reduction
        - Confusion damage reduction
        - Sleep/Freeze (cannot act)
        - Reflect/Light Screen defensive bonuses
        """
        action_type, action_obj = action

        if action_type == 'switch':
            return 0.0

        move = action_obj
        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon

        if not my_mon or not opp_mon:
            return 0.0

        # Cannot attack if asleep or frozen
        if my_mon.status in (Status.SLP, Status.FRZ):
            return 0.0

        # Handle special moves like "recharge"
        try:
            move_category = move.category.name
        except (KeyError, AttributeError):
            return 0.0

        # Status moves deal no damage
        if move_category == 'STATUS':
            return 0.0

        move_name = self._normalize_move_name(move.id)
        move_data = gen1_moves_dict.get(move_name, {})

        # Fixed damage moves
        if move.id in ['nightshade', 'seismictoss']:
            damage = my_mon.level
        elif move.id == 'dragonrage':
            damage = 40
        else:
            bp = move_data.get('bp', move.base_power)
            if bp == 0:
                return 0.0

            # Accuracy calculation
            if 'accuracy' in move_data:
                acc = move_data['accuracy'] / 100
            else:
                acc = 1.0
            acc *= self._get_accuracy_modifier(my_mon, opp_mon)
            acc = min(acc, 1.0)

            # Determine if special or physical
            move_type = move.type.name if move.type else 'Normal'
            is_special = move_type in self.SPECIAL_TYPES

            # Get attack stat with modifiers
            if is_special:
                atk_stat = self._get_stat_with_mods(my_mon, 'spa', is_own_pokemon=True)
                def_stat = self._get_opponent_def_stat(opp_mon, 'spd')
                # Light Screen doubles special defense
                if self._opponent_has_screen(battle, 'light_screen'):
                    def_stat *= 2
            else:
                atk_stat = self._get_stat_with_mods(my_mon, 'atk', is_own_pokemon=True)
                def_stat = self._get_opponent_def_stat(opp_mon, 'def')
                # Reflect doubles physical defense
                if self._opponent_has_screen(battle, 'reflect'):
                    def_stat *= 2

            # Gen 1 damage formula
            damage = ((2 * my_mon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
            damage *= 236 / 255  # Average random roll

            # STAB
            my_types = [t.name for t in my_mon.types if t]
            if move_type in my_types:
                damage *= 1.5

            # Type effectiveness
            opp_species = self._normalize_species_name(opp_mon.species)
            opp_types = gen1_mons_dict.get(opp_species, {}).get('types', ['Normal'])
            for opp_type in opp_types:
                damage *= type_effectiveness_dict.get(move_type, {}).get(opp_type, 1)

            # Apply accuracy
            damage *= acc

            # Paralysis reduces damage output
            if my_mon.status == Status.PAR:
                damage *= 0.75

            # Confusion has 50% chance of hitting self
            if self._is_confused(my_mon):
                damage *= 0.5

        # Calculate as fraction of opponent's max HP
        opp_max_hp = self._get_opponent_max_hp(opp_mon)
        damage_fraction = damage / opp_max_hp

        # Add opponent's expected self-confusion damage (they hit themselves 50% of the time)
        if self._is_confused(opp_mon):
            opp_self_damage = self._get_confusion_self_damage_opponent(opp_mon)
            damage_fraction += 0.5 * opp_self_damage / opp_max_hp

        return min(damage_fraction, 1.0)

    def _get_damage_received(self, battle: Battle, action: tuple) -> float:
        """
        Calculate expected damage received as fraction of target's max HP.

        For switches, calculates damage the switch target would receive.
        For moves, calculates damage the current active mon would receive.

        Accounts for all the same modifiers as damage done, but from opponent's perspective.
        """
        action_type, action_obj = action
        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon

        if not my_mon or not opp_mon:
            return 0.0

        # Opponent cannot attack if asleep or frozen
        if opp_mon.status in (Status.SLP, Status.FRZ):
            return 0.0

        # Determine which Pokemon will receive damage
        if action_type == 'switch':
            target = action_obj
        else:
            target = my_mon

        # Get opponent's known moves
        opp_moves = list(opp_mon.moves.values()) if opp_mon.moves else []
        if not opp_moves:
            # Default assumption if no moves known
            opp_moves = [self._create_default_move()]

        max_damage = 0
        for move in opp_moves:
            try:
                if move.category.name == 'STATUS':
                    continue
            except (KeyError, AttributeError):
                continue

            move_name = self._normalize_move_name(move.id)
            move_data = gen1_moves_dict.get(move_name, {})

            # Fixed damage moves
            if move.id in ['nightshade', 'seismictoss']:
                damage = opp_mon.level
            elif move.id == 'dragonrage':
                damage = 40
            else:
                bp = move_data.get('bp', move.base_power)
                if bp == 0:
                    continue

                # Accuracy
                if 'accuracy' in move_data:
                    acc = move_data['accuracy'] / 100
                else:
                    acc = 1.0
                acc *= self._get_accuracy_modifier(opp_mon, target, opp_attacking=True)
                acc = min(acc, 1.0)

                # Determine if special or physical
                move_type = move.type.name if move.type else 'Normal'
                is_special = move_type in self.SPECIAL_TYPES

                # Get attack/defense stats
                opp_species = self._normalize_species_name(opp_mon.species)
                if is_special:
                    atk_stat = self._get_opponent_atk_stat(opp_mon, 'spd')
                    def_stat = self._get_stat_with_mods(target, 'spd', is_own_pokemon=True)
                    # Our Light Screen doubles special defense (only if not switching)
                    if action_type != 'switch' and self._we_have_screen(battle, 'light_screen'):
                        def_stat *= 2
                else:
                    atk_stat = self._get_opponent_atk_stat(opp_mon, 'atk')
                    def_stat = self._get_stat_with_mods(target, 'def', is_own_pokemon=True)
                    # Our Reflect doubles physical defense (only if not switching)
                    if action_type != 'switch' and self._we_have_screen(battle, 'reflect'):
                        def_stat *= 2

                # Gen 1 damage formula
                damage = ((2 * opp_mon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
                damage *= 236 / 255

                # STAB for opponent
                opp_types = gen1_mons_dict.get(opp_species, {}).get('types', ['Normal'])
                if move_type in opp_types:
                    damage *= 1.5

                # Type effectiveness against target
                target_species = self._normalize_species_name(target.species)
                target_types = gen1_mons_dict.get(target_species, {}).get('types', ['Normal'])
                for target_type in target_types:
                    damage *= type_effectiveness_dict.get(move_type, {}).get(target_type, 1)

                # Apply accuracy
                damage *= acc

                # Opponent paralysis reduces their damage
                if opp_mon.status == Status.PAR:
                    damage *= 0.75

                # Opponent confusion reduces their damage
                if self._is_confused(opp_mon):
                    damage *= 0.5

            max_damage = max(max_damage, damage)

        target_max_hp = target.max_hp if target.max_hp else 100
        damage_fraction = max_damage / target_max_hp

        # Add our expected self-confusion damage (we hit ourselves 50% of the time when confused)
        # Use the mon that will be attacking (my_mon for moves, but for switches we still
        # need to consider if my_mon is confused and will attack before switching completes)
        if action_type != 'switch' and self._is_confused(my_mon):
            self_damage = self._get_confusion_self_damage(my_mon)
            damage_fraction += 0.5 * self_damage / (my_mon.max_hp if my_mon.max_hp else 100)

        return min(damage_fraction, 1.0)

    # ==================== Helper Methods ====================

    def _get_stat_with_mods(self, pokemon: Pokemon, stat: str, is_own_pokemon: bool = True) -> float:
        """Get a Pokemon's stat with boost modifiers applied."""
        if is_own_pokemon and pokemon.stats:
            # Use actual stats for our Pokemon
            # Map 'spa' to 'spd' for Gen 1 (Special stat)
            stat_key = 'spd' if stat == 'spa' else stat
            base_stat = pokemon.stats.get(stat_key, 80)
        else:
            # Estimate for opponent
            species = self._normalize_species_name(pokemon.species)
            bs = gen1_mons_dict.get(species, {}).get('bs', {})
            base_stat = bs.get(stat, 80)
            # Calculate stat from base
            base_stat = math.floor(((base_stat + 15) * 2 + 63) * pokemon.level / 100) + 5

        # Apply boost modifier: each stage is 1.5x multiplier
        boost = pokemon.boosts.get(stat, 0) if pokemon.boosts else 0
        # In Gen 1, spa and spd share the same boost
        if stat in ('spa', 'spd') and pokemon.boosts:
            boost = pokemon.boosts.get('spa', pokemon.boosts.get('spd', 0))

        return base_stat * (1.5 ** boost)

    def _get_opponent_speed(self, opp_mon: Pokemon) -> float:
        """Calculate opponent's speed with stat mods and paralysis."""
        species = self._normalize_species_name(opp_mon.species)
        base_spe = gen1_mons_dict.get(species, {}).get('bs', {}).get('spe', 80)
        speed = math.floor(((base_spe + 15) * 2 + 63) * opp_mon.level / 100) + 5

        # Apply speed boost
        boost = opp_mon.boosts.get('spe', 0) if opp_mon.boosts else 0
        speed *= (1.5 ** boost)

        # Paralysis quarters speed
        if opp_mon.status == Status.PAR:
            speed *= 0.25

        return speed

    def _get_opponent_def_stat(self, opp_mon: Pokemon, stat: str) -> float:
        """Get opponent's defensive stat with modifiers."""
        species = self._normalize_species_name(opp_mon.species)
        base = gen1_mons_dict.get(species, {}).get('bs', {}).get(stat, 80)
        def_stat = math.floor(((base + 15) * 2 + 63) * opp_mon.level / 100) + 5

        # Apply boost
        boost = opp_mon.boosts.get(stat, 0) if opp_mon.boosts else 0
        if stat in ('spa', 'spd') and opp_mon.boosts:
            boost = opp_mon.boosts.get('spa', opp_mon.boosts.get('spd', 0))

        return def_stat * (1.5 ** boost)

    def _get_opponent_atk_stat(self, opp_mon: Pokemon, stat: str) -> float:
        """Get opponent's attack stat with modifiers."""
        species = self._normalize_species_name(opp_mon.species)
        base = gen1_mons_dict.get(species, {}).get('bs', {}).get(stat, 80)
        atk_stat = math.floor(((base + 15) * 2 + 63) * opp_mon.level / 100) + 5

        # Apply boost
        boost = opp_mon.boosts.get(stat, 0) if opp_mon.boosts else 0
        if stat in ('spa', 'spd') and opp_mon.boosts:
            boost = opp_mon.boosts.get('spa', opp_mon.boosts.get('spd', 0))

        return atk_stat * (1.5 ** boost)

    def _get_opponent_max_hp(self, opp_mon: Pokemon) -> float:
        """Calculate opponent's probable max HP."""
        species = self._normalize_species_name(opp_mon.species)
        base_hp = gen1_mons_dict.get(species, {}).get('bs', {}).get('hp', 80)
        return math.floor(((base_hp + 15) * 2 + 63) * opp_mon.level / 100) + opp_mon.level + 10

    def _get_accuracy_modifier(self, attacker: Pokemon, defender: Pokemon, opp_attacking: bool = False) -> float:
        """Calculate accuracy modifier based on accuracy/evasion stat stages."""
        if opp_attacking:
            # Opponent attacking us
            acc_boost = attacker.boosts.get('accuracy', 0) if attacker.boosts else 0
            eva_boost = defender.boosts.get('evasion', 0) if defender.boosts else 0
        else:
            # We attacking opponent
            acc_boost = attacker.boosts.get('accuracy', 0) if attacker.boosts else 0
            eva_boost = defender.boosts.get('evasion', 0) if defender.boosts else 0

        return 1.5 ** (acc_boost - eva_boost)

    def _opponent_has_move(self, opp_mon: Pokemon, move_id: str) -> bool:
        """Check if opponent has a specific move in their known moveset."""
        if not opp_mon.moves:
            return False
        return move_id in opp_mon.moves

    def _opponent_has_screen(self, battle: Battle, screen: str) -> bool:
        """Check if opponent has Reflect or Light Screen up."""
        if screen == 'reflect':
            return SideCondition.REFLECT in battle.opponent_side_conditions
        elif screen == 'light_screen':
            return SideCondition.LIGHT_SCREEN in battle.opponent_side_conditions
        return False

    def _we_have_screen(self, battle: Battle, screen: str) -> bool:
        """Check if we have Reflect or Light Screen up."""
        if screen == 'reflect':
            return SideCondition.REFLECT in battle.side_conditions
        elif screen == 'light_screen':
            return SideCondition.LIGHT_SCREEN in battle.side_conditions
        return False

    def _is_confused(self, pokemon: Pokemon) -> bool:
        """Check if a Pokemon is confused."""
        if pokemon.effects:
            return Effect.CONFUSION in pokemon.effects
        return False

    def _get_confusion_self_damage(self, pokemon: Pokemon) -> float:
        """
        Calculate the damage a Pokemon deals to itself when hitting itself in confusion.

        In Gen 1, confusion self-hit is a 40 BP typeless physical attack
        using the Pokemon's Attack vs its own Defense.

        Returns damage as a raw value (not fraction of HP).
        """
        # 40 BP typeless attack
        bp = 40

        # Get Attack and Defense stats with modifiers
        atk_stat = self._get_stat_with_mods(pokemon, 'atk', is_own_pokemon=True)
        def_stat = self._get_stat_with_mods(pokemon, 'def', is_own_pokemon=True)

        # Gen 1 damage formula (no STAB, no type effectiveness for confusion)
        damage = ((2 * pokemon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
        damage *= 236 / 255  # Average random roll

        return damage

    def _get_confusion_self_damage_opponent(self, opp_mon: Pokemon) -> float:
        """
        Calculate the damage an opponent Pokemon deals to itself in confusion.

        Same as _get_confusion_self_damage but uses estimated opponent stats.

        Returns damage as a raw value (not fraction of HP).
        """
        # 40 BP typeless attack
        bp = 40

        # Get opponent's Attack and Defense stats (estimated)
        atk_stat = self._get_opponent_atk_stat(opp_mon, 'atk')
        def_stat = self._get_opponent_def_stat(opp_mon, 'def')

        # Gen 1 damage formula (no STAB, no type effectiveness for confusion)
        damage = ((2 * opp_mon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
        damage *= 236 / 255  # Average random roll

        return damage

    def _normalize_species_name(self, species: str) -> str:
        """Normalize species name to match gen1_mons_dict keys."""
        # Handle common variations
        name = species.replace('-', '').replace(' ', '').title()
        # Special cases
        if name == 'Mrmime':
            return 'Mr. Mime'
        if name == 'Farfetchd':
            return 'Farfetch\u2019d'
        if name == 'Nidoranf':
            return 'Nidoran-F'
        if name == 'Nidoranm':
            return 'Nidoran-M'
        return name

    def _normalize_move_name(self, move_id: str) -> str:
        """Normalize move ID to match gen1_moves_dict keys."""
        # Convert from poke-env format (lowercase, no spaces) to our format
        name = move_id.replace('_', ' ').replace('-', ' ').title()
        # Handle special cases
        if name == 'Doubleedge':
            return 'Double-Edge'
        if name == 'Softboiled':
            return 'Soft-Boiled'
        if name == 'Selfdestruct':
            return 'Self-Destruct'
        return name

    def _create_default_move(self):
        """Create a default move assumption when opponent's moves are unknown."""
        # Return a simple object that mimics a Move for Body Slam
        class DefaultMove:
            id = 'bodyslam'
            category = type('Category', (), {'name': 'Physical'})()
            type = type('Type', (), {'name': 'Normal'})()
            base_power = 85
        return DefaultMove()
