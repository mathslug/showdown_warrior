#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared feature engineering for Gen 1 Pokemon battle decisions.

This module handles all the calculation logic shared across thinkers:
- Damage calculations (with stat mods, status effects, screens)
- Outspeed probability calculations
- Status move value calculations
- Helper functions for stats, type effectiveness, etc.
"""
import math
from poke_env.battle import Pokemon, Move, Battle, Status, SideCondition, Effect

from general_poke_data import gen1_mons_dict, gen1_moves_dict, type_effectiveness_dict


# Types that use Special stat in Gen 1
SPECIAL_TYPES = frozenset(['Grass', 'Psychic', 'Ice', 'Water', 'Dragon', 'Fire', 'Electric', 'Dark'])

# Gen 1 partial-trapping moves (opponent cannot act while trapped)
GEN1_TRAPPING_MOVES = frozenset({'wrap', 'bind', 'firespin', 'clamp'})
EXPECTED_TRAP_TURNS = 3.0

# Feature columns used by all thinkers
FEATURE_COLS = ['self_hp', 'opp_hp', 'outspeed_prob', 'is_status_move',
                'exp_damage_done', 'exp_damage_received']


def compute_features(battle: Battle, action: tuple) -> dict:
    """
    Compute all features for a given action.

    Args:
        battle: Current battle state from poke-env
        action: Tuple of (action_type, action_obj) where action_type is 'move' or 'switch'

    Returns:
        Dictionary with all calculated features (excluding predicted_npw_score)
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
    m['outspeed_prob'] = _get_outspeed_prob(battle, action)
    m['is_status_move'] = _get_status_move_value(battle, action)
    m['exp_damage_done'] = _get_damage_done(battle, action)
    m['exp_damage_received'] = _get_damage_received(battle, action)

    return m


def _get_outspeed_prob(battle: Battle, action: tuple) -> float:
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
    my_speed = _get_stat_with_mods(my_mon, 'spe', is_own_pokemon=True)
    if my_mon.status == Status.PAR:
        my_speed *= 0.25

    # Calculate opponent speed with stat mods and paralysis
    opp_speed = _get_opponent_speed(opp_mon)

    # Check opponent's known moves for Counter/Quick Attack
    opp_has_counter = _opponent_has_move(opp_mon, 'counter')
    opp_has_quick_attack = _opponent_has_move(opp_mon, 'quickattack')

    if opp_speed > my_speed:
        if opp_has_counter:
            return 0.25
        return 0.0
    elif opp_speed == my_speed:
        if opp_has_counter and opp_has_quick_attack:
            return 0.5
        elif opp_has_counter:
            return 0.375
        elif opp_has_quick_attack:
            return 0.625
        return 0.5
    else:
        if opp_has_quick_attack:
            return 0.75
        return 1.0


def _get_status_move_value(battle: Battle, action: tuple) -> float:
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

    try:
        move_category = move.category.name
    except (KeyError, AttributeError):
        return 0.0

    move_name = _normalize_move_name(move.id)
    move_data = gen1_moves_dict.get(move_name, {})

    if move_category == 'STATUS':
        if 'accuracy' in move_data:
            base_acc = move_data['accuracy'] / 100
        else:
            base_acc = 1.0
        acc_mod = _get_accuracy_modifier(my_mon, opp_mon)
        return min(base_acc * acc_mod, 1.0)

    elif 'statusperc' in move_data:
        if 'accuracy' in move_data:
            base_acc = move_data['accuracy'] / 100
        else:
            base_acc = 1.0
        status_chance = move_data['statusperc'] / 100
        acc_mod = _get_accuracy_modifier(my_mon, opp_mon)
        return min(base_acc * acc_mod * status_chance, 1.0)

    return 0.0


def _get_damage_done(battle: Battle, action: tuple) -> float:
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

    if my_mon.status in (Status.SLP, Status.FRZ):
        return 0.0

    try:
        move_category = move.category.name
    except (KeyError, AttributeError):
        return 0.0

    if move_category == 'STATUS':
        return 0.0

    move_name = _normalize_move_name(move.id)
    move_data = gen1_moves_dict.get(move_name, {})

    if move.id in ['nightshade', 'seismictoss']:
        damage = my_mon.level
    elif move.id == 'dragonrage':
        damage = 40
    else:
        bp = move_data.get('bp', move.base_power)
        if bp == 0:
            return 0.0

        if 'accuracy' in move_data:
            acc = move_data['accuracy'] / 100
        else:
            acc = 1.0
        acc *= _get_accuracy_modifier(my_mon, opp_mon)
        acc = min(acc, 1.0)

        move_type = move.type.name if move.type else 'Normal'
        is_special = move_type in SPECIAL_TYPES

        if is_special:
            atk_stat = _get_stat_with_mods(my_mon, 'spa', is_own_pokemon=True)
            def_stat = _get_opponent_def_stat(opp_mon, 'spd')
            if _opponent_has_screen(battle, 'light_screen'):
                def_stat *= 2
        else:
            atk_stat = _get_stat_with_mods(my_mon, 'atk', is_own_pokemon=True)
            def_stat = _get_opponent_def_stat(opp_mon, 'def')
            if _opponent_has_screen(battle, 'reflect'):
                def_stat *= 2

        if move.id in ('explosion', 'selfdestruct'):
            def_stat /= 2

        damage = ((2 * my_mon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
        damage *= 236 / 255

        my_types = [t.name for t in my_mon.types if t]
        if move_type in my_types:
            damage *= 1.5

        opp_species = _normalize_species_name(opp_mon.species)
        opp_types = gen1_mons_dict.get(opp_species, {}).get('types', ['Normal'])
        for opp_type in opp_types:
            damage *= type_effectiveness_dict.get(move_type, {}).get(opp_type, 1)

        damage *= acc

        if my_mon.status == Status.PAR:
            damage *= 0.75

        if _is_confused(my_mon):
            damage *= 0.5

        damage *= move.expected_hits

        if move.id in GEN1_TRAPPING_MOVES:
            damage *= EXPECTED_TRAP_TURNS

    opp_max_hp = _get_opponent_max_hp(opp_mon)
    damage_fraction = damage / opp_max_hp

    if _is_confused(opp_mon):
        opp_self_damage = _get_confusion_self_damage_opponent(opp_mon)
        damage_fraction += 0.5 * opp_self_damage / opp_max_hp

    return min(damage_fraction, opp_mon.current_hp_fraction)


def _get_damage_received(battle: Battle, action: tuple) -> float:
    """
    Calculate expected damage received as fraction of target's max HP.

    For switches, calculates damage the switch target would receive.
    For moves, calculates damage the current active mon would receive.
    """
    action_type, action_obj = action
    my_mon = battle.active_pokemon
    opp_mon = battle.opponent_active_pokemon

    if not my_mon or not opp_mon:
        return 0.0

    if action_type == 'move' and action_obj.id in ('explosion', 'selfdestruct'):
        return my_mon.current_hp_fraction if my_mon else 1.0

    if opp_mon.status in (Status.SLP, Status.FRZ):
        return 0.0

    if action_type == 'switch':
        target = action_obj
    else:
        target = my_mon

    opp_moves = list(opp_mon.moves.values()) if opp_mon.moves else []
    if not opp_moves:
        opp_moves = [_create_default_move()]

    max_damage = 0
    for move in opp_moves:
        try:
            if move.category.name == 'STATUS':
                continue
        except (KeyError, AttributeError):
            continue

        move_name = _normalize_move_name(move.id)
        move_data = gen1_moves_dict.get(move_name, {})

        if move.id in ['nightshade', 'seismictoss']:
            damage = opp_mon.level
        elif move.id == 'dragonrage':
            damage = 40
        else:
            bp = move_data.get('bp', move.base_power)
            if bp == 0:
                continue

            if 'accuracy' in move_data:
                acc = move_data['accuracy'] / 100
            else:
                acc = 1.0
            acc *= _get_accuracy_modifier(opp_mon, target, opp_attacking=True)
            acc = min(acc, 1.0)

            move_type = move.type.name if move.type else 'Normal'
            is_special = move_type in SPECIAL_TYPES

            opp_species = _normalize_species_name(opp_mon.species)
            if is_special:
                atk_stat = _get_opponent_atk_stat(opp_mon, 'spd')
                def_stat = _get_stat_with_mods(target, 'spd', is_own_pokemon=True)
                if action_type != 'switch' and _we_have_screen(battle, 'light_screen'):
                    def_stat *= 2
            else:
                atk_stat = _get_opponent_atk_stat(opp_mon, 'atk')
                def_stat = _get_stat_with_mods(target, 'def', is_own_pokemon=True)
                if action_type != 'switch' and _we_have_screen(battle, 'reflect'):
                    def_stat *= 2

            damage = ((2 * opp_mon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
            damage *= 236 / 255

            opp_types = gen1_mons_dict.get(opp_species, {}).get('types', ['Normal'])
            if move_type in opp_types:
                damage *= 1.5

            target_species = _normalize_species_name(target.species)
            target_types = gen1_mons_dict.get(target_species, {}).get('types', ['Normal'])
            for target_type in target_types:
                damage *= type_effectiveness_dict.get(move_type, {}).get(target_type, 1)

            damage *= acc

            if opp_mon.status == Status.PAR:
                damage *= 0.75

            if _is_confused(opp_mon):
                damage *= 0.5

            damage *= move.expected_hits

            if move.id in GEN1_TRAPPING_MOVES:
                damage *= EXPECTED_TRAP_TURNS

        max_damage = max(max_damage, damage)

    target_max_hp = target.max_hp if target.max_hp else 100
    damage_fraction = max_damage / target_max_hp

    if action_type != 'switch' and _is_confused(my_mon):
        self_damage = _get_confusion_self_damage(my_mon)
        damage_fraction += 0.5 * self_damage / (my_mon.max_hp if my_mon.max_hp else 100)

    return min(damage_fraction, target.current_hp_fraction)


# ==================== Helper Functions ====================

def _boost_multiplier(boost: int) -> float:
    """Apply Gen 1 stat stage multiplier."""
    if boost >= 0:
        return (2 + boost) / 2
    else:
        return 2 / (2 - boost)


def _acc_eva_multiplier(stage: int) -> float:
    """Apply Gen 1 accuracy/evasion stage multiplier."""
    if stage >= 0:
        return (3 + stage) / 3
    else:
        return 3 / (3 - stage)


def _get_stat_with_mods(pokemon: Pokemon, stat: str, is_own_pokemon: bool = True) -> float:
    """Get a Pokemon's stat with boost modifiers applied."""
    if is_own_pokemon and pokemon.stats:
        stat_key = 'spd' if stat == 'spa' else stat
        base_stat = pokemon.stats.get(stat_key, 80)
    else:
        species = _normalize_species_name(pokemon.species)
        bs = gen1_mons_dict.get(species, {}).get('bs', {})
        base_stat = bs.get(stat, 80)
        base_stat = math.floor(((base_stat + 15) * 2 + 63) * pokemon.level / 100) + 5

    boost = pokemon.boosts.get(stat, 0) if pokemon.boosts else 0
    if stat in ('spa', 'spd') and pokemon.boosts:
        boost = pokemon.boosts.get('spa', pokemon.boosts.get('spd', 0))

    return base_stat * _boost_multiplier(boost)


def _get_opponent_speed(opp_mon: Pokemon) -> float:
    """Calculate opponent's speed with stat mods and paralysis."""
    species = _normalize_species_name(opp_mon.species)
    base_spe = gen1_mons_dict.get(species, {}).get('bs', {}).get('spe', 80)
    speed = math.floor(((base_spe + 15) * 2 + 63) * opp_mon.level / 100) + 5

    boost = opp_mon.boosts.get('spe', 0) if opp_mon.boosts else 0
    speed *= _boost_multiplier(boost)

    if opp_mon.status == Status.PAR:
        speed *= 0.25

    return speed


def _get_opponent_def_stat(opp_mon: Pokemon, stat: str) -> float:
    """Get opponent's defensive stat with modifiers."""
    species = _normalize_species_name(opp_mon.species)
    base = gen1_mons_dict.get(species, {}).get('bs', {}).get(stat, 80)
    def_stat = math.floor(((base + 15) * 2 + 63) * opp_mon.level / 100) + 5

    boost = opp_mon.boosts.get(stat, 0) if opp_mon.boosts else 0
    if stat in ('spa', 'spd') and opp_mon.boosts:
        boost = opp_mon.boosts.get('spa', opp_mon.boosts.get('spd', 0))

    return def_stat * _boost_multiplier(boost)


def _get_opponent_atk_stat(opp_mon: Pokemon, stat: str) -> float:
    """Get opponent's attack stat with modifiers."""
    species = _normalize_species_name(opp_mon.species)
    base = gen1_mons_dict.get(species, {}).get('bs', {}).get(stat, 80)
    atk_stat = math.floor(((base + 15) * 2 + 63) * opp_mon.level / 100) + 5

    boost = opp_mon.boosts.get(stat, 0) if opp_mon.boosts else 0
    if stat in ('spa', 'spd') and opp_mon.boosts:
        boost = opp_mon.boosts.get('spa', opp_mon.boosts.get('spd', 0))

    return atk_stat * _boost_multiplier(boost)


def _get_opponent_max_hp(opp_mon: Pokemon) -> float:
    """Calculate opponent's probable max HP."""
    species = _normalize_species_name(opp_mon.species)
    base_hp = gen1_mons_dict.get(species, {}).get('bs', {}).get('hp', 80)
    return math.floor(((base_hp + 15) * 2 + 63) * opp_mon.level / 100) + opp_mon.level + 10


def _get_accuracy_modifier(attacker: Pokemon, defender: Pokemon, opp_attacking: bool = False) -> float:
    """Calculate accuracy modifier based on accuracy/evasion stat stages."""
    acc_boost = attacker.boosts.get('accuracy', 0) if attacker.boosts else 0
    eva_boost = defender.boosts.get('evasion', 0) if defender.boosts else 0
    combined = max(-6, min(6, acc_boost - eva_boost))
    return _acc_eva_multiplier(combined)


def _opponent_has_move(opp_mon: Pokemon, move_id: str) -> bool:
    """Check if opponent has a specific move in their known moveset."""
    if not opp_mon.moves:
        return False
    return move_id in opp_mon.moves


def _opponent_has_screen(battle: Battle, screen: str) -> bool:
    """Check if opponent has Reflect or Light Screen up."""
    if screen == 'reflect':
        return SideCondition.REFLECT in battle.opponent_side_conditions
    elif screen == 'light_screen':
        return SideCondition.LIGHT_SCREEN in battle.opponent_side_conditions
    return False


def _we_have_screen(battle: Battle, screen: str) -> bool:
    """Check if we have Reflect or Light Screen up."""
    if screen == 'reflect':
        return SideCondition.REFLECT in battle.side_conditions
    elif screen == 'light_screen':
        return SideCondition.LIGHT_SCREEN in battle.side_conditions
    return False


def _is_confused(pokemon: Pokemon) -> bool:
    """Check if a Pokemon is confused."""
    if pokemon.effects:
        return Effect.CONFUSION in pokemon.effects
    return False


def _get_confusion_self_damage(pokemon: Pokemon) -> float:
    """Calculate the damage a Pokemon deals to itself in confusion."""
    bp = 40
    atk_stat = _get_stat_with_mods(pokemon, 'atk', is_own_pokemon=True)
    def_stat = _get_stat_with_mods(pokemon, 'def', is_own_pokemon=True)
    damage = ((2 * pokemon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
    damage *= 236 / 255
    return damage


def _get_confusion_self_damage_opponent(opp_mon: Pokemon) -> float:
    """Calculate the damage an opponent Pokemon deals to itself in confusion."""
    bp = 40
    atk_stat = _get_opponent_atk_stat(opp_mon, 'atk')
    def_stat = _get_opponent_def_stat(opp_mon, 'def')
    damage = ((2 * opp_mon.level / 5 + 2) * bp * atk_stat / def_stat / 50 + 2)
    damage *= 236 / 255
    return damage


def _normalize_species_name(species: str) -> str:
    """Normalize species name to match gen1_mons_dict keys."""
    name = species.replace('-', '').replace(' ', '').title()
    if name == 'Mrmime':
        return 'Mr. Mime'
    if name == 'Farfetchd':
        return 'Farfetch\u2019d'
    if name == 'Nidoranf':
        return 'Nidoran-F'
    if name == 'Nidoranm':
        return 'Nidoran-M'
    return name


def _normalize_move_name(move_id: str) -> str:
    """Normalize move ID to match gen1_moves_dict keys."""
    name = move_id.replace('_', ' ').replace('-', ' ').title()
    if name == 'Doubleedge':
        return 'Double-Edge'
    if name == 'Softboiled':
        return 'Soft-Boiled'
    if name == 'Selfdestruct':
        return 'Self-Destruct'
    return name


def _create_default_move():
    """Create a default move assumption when opponent's moves are unknown."""
    class DefaultMove:
        id = 'bodyslam'
        category = type('Category', (), {'name': 'Physical'})()
        type = type('Type', (), {'name': 'Normal'})()
        base_power = 85
        expected_hits = 1.0
    return DefaultMove()
