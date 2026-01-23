#!/usr/bin/env python3
import logging
import math
import orjson
import random
import time
import pandas as pd
from os import path
from sklearn.neighbors import KNeighborsRegressor

from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.player import Player
from poke_env.battle import Battle, Pokemon, Move

from general_poke_data import gen1_mons_dict, gen1_moves_dict, type_effectiveness_dict


class Gen1WarriorPlayer(Player):

    def __init__(self, username, password, training_mode=False, max_concurrent_battles=5, log_level=logging.INFO, **kwargs):
        super().__init__(
            account_configuration=AccountConfiguration(username, password),
            battle_format="gen1randombattle",
            server_configuration=ShowdownServerConfiguration,
            max_concurrent_battles=max_concurrent_battles,
            log_level=log_level,
            **kwargs
        )
        self.training_mode = training_mode
        self.turn_counter = 0
        self._battle_metrics = self._empty_metrics()
        self._username = username

        if path.exists('./data/battle_records.csv'):
            self._training_data = pd.read_csv('./data/battle_records.csv', index_col=False)
            n_neighbors = max(1, math.floor(math.sqrt(self._training_data.shape[0])))
            self._knner = KNeighborsRegressor(n_neighbors=n_neighbors).fit(
                self._training_data[['self_hp', 'opp_hp', 'outspeed_prob',
                                     'is_status_move', 'exp_damage_done',
                                     'exp_damage_received']],
                self._training_data.actual_npw_score
            )
            self._knnpred = lambda df: self._knner.predict(df)[0]
        else:
            self._training_data = pd.DataFrame()
            self._knnpred = lambda df: 0

    def _empty_metrics(self):
        return {k: [] for k in ['turn', 'action', 'self_hp', 'opp_hp', 'outspeed_prob',
                                'is_status_move', 'exp_damage_done', 'exp_damage_received',
                                'predicted_npw_score']}

    def choose_move(self, battle):
        self.turn_counter = battle.turn
        actions = [('move', m) for m in battle.available_moves] + \
                  [('switch', p) for p in battle.available_switches]

        if not actions:
            return self.choose_random_move(battle)

        action_metrics = [self._get_action_metrics(battle, a) for a in actions]

        print("\nCHOICES:")
        for idx, m in enumerate(action_metrics):
            print(f"  {idx + 1}: {m['action_name']} (score: {m['predicted_npw_score']:.3f})")

        if self.training_mode:
            print("")
            try:
                user_inp = int(input('What should we do? '))
                selected_idx = max(0, min(user_inp - 1, len(action_metrics) - 1))
            except (ValueError, EOFError):
                selected_idx = 0
            selected = action_metrics[selected_idx]
        else:
            max_score = max(m['predicted_npw_score'] for m in action_metrics)
            best = [m for m in action_metrics if m['predicted_npw_score'] == max_score]
            selected = random.choice(best)
            time.sleep(1.5)

        self._record_action(selected)
        return selected['battle_order']

    def _get_action_metrics(self, battle, action):
        action_type, action_obj = action
        m = {}

        if action_type == 'move':
            m['is_switch'] = False
            m['action_name'] = action_obj.id
            m['battle_order'] = self.create_order(action_obj)
        else:
            m['is_switch'] = True
            m['action_name'] = action_obj.species
            m['battle_order'] = self.create_order(action_obj)

        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon

        m['self_hp'] = my_mon.current_hp_fraction if my_mon else 1.0
        m['opp_hp'] = opp_mon.current_hp_fraction if opp_mon else 1.0
        m['outspeed_prob'] = self._get_outspeed_prob(battle, action)
        m['is_status_move'] = self._get_status_move_value(action)
        m['exp_damage_done'] = self._get_damage_done(battle, action)
        m['exp_damage_received'] = self._get_damage_received(battle, action)

        metrics_df = pd.DataFrame({k: [m[k]] for k in ['self_hp', 'opp_hp', 'outspeed_prob',
                                                        'is_status_move', 'exp_damage_done',
                                                        'exp_damage_received']})
        m['predicted_npw_score'] = self._knnpred(metrics_df)
        return m

    def _get_outspeed_prob(self, battle, action):
        action_type, action_obj = action
        if action_type == 'switch':
            return 1.0

        move = action_obj
        try:
            if move.priority > 0:
                return 1.0
        except (KeyError, AttributeError):
            pass
        if move.id == 'counter':
            return 0.0

        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon
        if not my_mon or not opp_mon:
            return 0.5

        my_speed = my_mon.stats.get('spe', 100) if my_mon.stats else 100
        if my_mon.status and my_mon.status.name == 'PAR':
            my_speed *= 0.25

        opp_species = opp_mon.species.replace('-', '').replace(' ', '').title()
        opp_base = gen1_mons_dict.get(opp_species, {}).get('bs', {}).get('spe', 80)
        opp_speed = math.floor(((opp_base + 15) * 2 + 63) * opp_mon.level / 100) + 5
        if opp_mon.status and opp_mon.status.name == 'PAR':
            opp_speed *= 0.25

        if opp_speed > my_speed:
            return 0.0
        elif opp_speed == my_speed:
            return 0.5
        return 1.0

    def _get_status_move_value(self, action):
        action_type, action_obj = action
        if action_type == 'switch':
            return 0.0

        move = action_obj
        move_data = gen1_moves_dict.get(move.id.replace('_', ' ').title(), {})

        try:
            if move.category.name == 'STATUS':
                return move_data.get('accuracy', 100) / 100 if 'accuracy' in move_data else 1.0
        except (KeyError, AttributeError):
            return 0.0
        if 'statusperc' in move_data:
            acc = move_data.get('accuracy', 100) / 100
            return acc * move_data['statusperc'] / 100
        return 0.0

    def _get_damage_done(self, battle, action):
        action_type, action_obj = action
        if action_type == 'switch':
            return 0.0

        move = action_obj
        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon
        if not my_mon or not opp_mon:
            return 0.0

        try:
            if move.category.name == 'STATUS':
                return 0.0
        except (KeyError, AttributeError):
            return 0.0

        if move.id in ['nightshade', 'seismictoss']:
            damage = my_mon.level
        elif move.id == 'dragonrage':
            damage = 40
        else:
            move_data = gen1_moves_dict.get(move.id.replace('_', ' ').title(), {})
            bp = move_data.get('bp', move.base_power)
            if bp == 0:
                return 0.0

            acc = move_data.get('accuracy', 100) / 100 if 'accuracy' in move_data else 1.0
            move_type = move.type.name if move.type else 'Normal'
            special_types = ['Grass', 'Psychic', 'Ice', 'Water', 'Dragon', 'Fire', 'Electric', 'Dark']

            if move_type in special_types:
                atk_stat = my_mon.stats.get('spa', 80) if my_mon.stats else 80
                opp_species = opp_mon.species.replace('-', '').replace(' ', '').title()
                opp_base_def = gen1_mons_dict.get(opp_species, {}).get('bs', {}).get('spd', 80)
            else:
                atk_stat = my_mon.stats.get('atk', 80) if my_mon.stats else 80
                opp_species = opp_mon.species.replace('-', '').replace(' ', '').title()
                opp_base_def = gen1_mons_dict.get(opp_species, {}).get('bs', {}).get('def', 80)

            def_stat = math.floor(((opp_base_def + 15) * 2 + 63) * opp_mon.level / 100) + 5
            damage = ((2 * my_mon.level / 5 + 2) * bp * acc * atk_stat / def_stat / 50 + 2) * 236 / 255

            my_types = [t.name for t in my_mon.types if t]
            if move_type in my_types:
                damage *= 1.5

            opp_types = [t.name for t in opp_mon.types if t]
            for ot in opp_types:
                damage *= type_effectiveness_dict.get(move_type, {}).get(ot, 1)

        opp_species = opp_mon.species.replace('-', '').replace(' ', '').title()
        opp_base_hp = gen1_mons_dict.get(opp_species, {}).get('bs', {}).get('hp', 80)
        opp_max_hp = math.floor(((opp_base_hp + 15) * 2 + 63) * opp_mon.level / 100) + opp_mon.level + 10
        return min(damage / opp_max_hp, 1.0)

    def _get_damage_received(self, battle, action):
        action_type, action_obj = action
        my_mon = battle.active_pokemon
        opp_mon = battle.opponent_active_pokemon
        if not my_mon or not opp_mon:
            return 0.0

        target = action_obj if action_type == 'switch' else my_mon
        opp_moves = list(opp_mon.moves.values()) if opp_mon.moves else []
        if not opp_moves:
            return 0.3

        max_damage = 0
        for move in opp_moves:
            if move.category.name == 'STATUS':
                continue

            move_data = gen1_moves_dict.get(move.id.replace('_', ' ').title(), {})
            bp = move_data.get('bp', move.base_power)
            if bp == 0:
                continue

            acc = move_data.get('accuracy', 100) / 100 if 'accuracy' in move_data else 1.0
            move_type = move.type.name if move.type else 'Normal'
            special_types = ['Grass', 'Psychic', 'Ice', 'Water', 'Dragon', 'Fire', 'Electric', 'Dark']

            opp_species = opp_mon.species.replace('-', '').replace(' ', '').title()
            if move_type in special_types:
                opp_base_atk = gen1_mons_dict.get(opp_species, {}).get('bs', {}).get('spd', 80)
                def_stat = target.stats.get('spd', 80) if target.stats else 80
            else:
                opp_base_atk = gen1_mons_dict.get(opp_species, {}).get('bs', {}).get('atk', 80)
                def_stat = target.stats.get('def', 80) if target.stats else 80

            atk_stat = math.floor(((opp_base_atk + 15) * 2 + 63) * opp_mon.level / 100) + 5
            damage = ((2 * opp_mon.level / 5 + 2) * bp * acc * atk_stat / def_stat / 50 + 2) * 236 / 255

            opp_types = [t.name for t in opp_mon.types if t]
            if move_type in opp_types:
                damage *= 1.5

            target_types = [t.name for t in target.types if t]
            for tt in target_types:
                damage *= type_effectiveness_dict.get(move_type, {}).get(tt, 1)

            max_damage = max(max_damage, damage)

        return min(max_damage / (target.max_hp or 100), 1.0)

    def _record_action(self, m):
        self._battle_metrics['turn'].append(self.turn_counter)
        self._battle_metrics['action'].append(m['action_name'])
        self._battle_metrics['self_hp'].append(m['self_hp'])
        self._battle_metrics['opp_hp'].append(m['opp_hp'])
        self._battle_metrics['outspeed_prob'].append(m['outspeed_prob'])
        self._battle_metrics['is_status_move'].append(m['is_status_move'])
        self._battle_metrics['exp_damage_done'].append(m['exp_damage_done'])
        self._battle_metrics['exp_damage_received'].append(m['exp_damage_received'])
        self._battle_metrics['predicted_npw_score'].append(m['predicted_npw_score'])

    def _battle_finished_callback(self, battle):
        won = battle.won
        is_tie = won is None
        knight_wins = True if is_tie else won

        print(f"\nBattle finished! {'Win' if knight_wins else 'Loss'}{' (tie)' if is_tie else ''}")

        if self._battle_metrics['turn']:
            final_turn = max(self._battle_metrics['turn'])
            self._battle_metrics['actual_npw_score'] = [
                (knight_wins / 1.1 ** (final_turn - t)) / (2 if is_tie else 1)
                for t in self._battle_metrics['turn']
            ]
            battle_frame = pd.DataFrame.from_dict(self._battle_metrics)
            all_data = pd.concat([battle_frame, self._training_data], ignore_index=True, sort=False)
            all_data.to_csv('./data/battle_records.csv', index=False)
            print(f"Saved {len(all_data)} records")

        self._battle_metrics = self._empty_metrics()
        self.turn_counter = 0
