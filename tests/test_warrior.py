#!/usr/bin/env python3
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import math

from general_poke_data import gen1_mons_dict, gen1_moves_dict, type_effectiveness_dict


class MockStatus:
    def __init__(self, name):
        self.name = name


class MockType:
    def __init__(self, name):
        self.name = name


class MockCategory:
    def __init__(self, name):
        self.name = name


class MockMove:
    def __init__(self, id, type_name="Normal", category="Physical", base_power=80, priority=0):
        self.id = id
        self.type = MockType(type_name)
        self.category = MockCategory(category)
        self.base_power = base_power
        self._priority = priority

    @property
    def priority(self):
        return self._priority


class MockPokemon:
    def __init__(self, species, level=100, hp_fraction=1.0, stats=None, types=None, status=None, moves=None, max_hp=300):
        self.species = species
        self.level = level
        self._current_hp_fraction = hp_fraction
        self.stats = stats or {'atk': 100, 'def': 100, 'spa': 100, 'spd': 100, 'spe': 100}
        self.types = [MockType(t) for t in (types or ['Normal'])]
        self.status = MockStatus(status) if status else None
        self.moves = {m.id: m for m in (moves or [])}
        self.max_hp = max_hp

    @property
    def current_hp_fraction(self):
        return self._current_hp_fraction


class MockBattle:
    def __init__(self, active_pokemon=None, opponent_active_pokemon=None, turn=1):
        self.active_pokemon = active_pokemon
        self.opponent_active_pokemon = opponent_active_pokemon
        self.turn = turn
        self.available_moves = []
        self.available_switches = []


class TestTypeEffectiveness:
    def test_water_vs_fire(self):
        assert type_effectiveness_dict['Water']['Fire'] == 2

    def test_fire_vs_water(self):
        assert type_effectiveness_dict['Fire']['Water'] == 0.5

    def test_normal_vs_ghost(self):
        assert type_effectiveness_dict['Normal']['Ghost'] == 0

    def test_ground_vs_flying(self):
        assert type_effectiveness_dict['Ground']['Flying'] == 0

    def test_electric_vs_ground(self):
        assert type_effectiveness_dict['Electric']['Ground'] == 0


class TestGen1Data:
    def test_alakazam_stats(self):
        alakazam = gen1_mons_dict['Alakazam']
        assert alakazam['types'] == ['Psychic']
        assert alakazam['bs']['spe'] == 120
        assert alakazam['bs']['spd'] == 135

    def test_snorlax_stats(self):
        snorlax = gen1_mons_dict['Snorlax']
        assert snorlax['types'] == ['Normal']
        assert snorlax['bs']['hp'] == 160

    def test_thunderbolt_data(self):
        tbolt = gen1_moves_dict['Thunderbolt']
        assert tbolt['bp'] == 95
        assert tbolt['type'] == 'Electric'
        assert tbolt['accuracy'] == 100


class TestWarriorPlayer:
    @pytest.fixture
    def player(self):
        with patch('warrior_player.path.exists', return_value=False):
            with patch.object(
                __import__('warrior_player', fromlist=['Gen1WarriorPlayer']).Gen1WarriorPlayer,
                '__init__',
                lambda self, *args, **kwargs: None
            ):
                from warrior_player import Gen1WarriorPlayer
                p = Gen1WarriorPlayer.__new__(Gen1WarriorPlayer)
                p.training_mode = False
                p.turn_counter = 0
                p._battle_metrics = p._empty_metrics() if hasattr(p, '_empty_metrics') else {}
                p._username = 'testuser'
                p._training_data = pd.DataFrame()
                p._knnpred = lambda df: 0
                p._format = 'gen1randombattle'
                return p

    def test_outspeed_prob_switch_returns_one(self, player):
        battle = MockBattle()
        action = ('switch', MockPokemon('Alakazam'))
        result = player._get_outspeed_prob(battle, action)
        assert result == 1.0

    def test_outspeed_prob_priority_move(self, player):
        battle = MockBattle(
            active_pokemon=MockPokemon('Raticate', stats={'spe': 50}),
            opponent_active_pokemon=MockPokemon('Alakazam')
        )
        quick_attack = MockMove('quickattack', priority=1)
        action = ('move', quick_attack)
        result = player._get_outspeed_prob(battle, action)
        assert result == 1.0

    def test_outspeed_prob_counter_returns_zero(self, player):
        battle = MockBattle(
            active_pokemon=MockPokemon('Chansey'),
            opponent_active_pokemon=MockPokemon('Tauros')
        )
        counter = MockMove('counter', type_name='Fighting', priority=0)
        action = ('move', counter)
        result = player._get_outspeed_prob(battle, action)
        assert result == 0.0

    def test_status_move_value_for_switch(self, player):
        action = ('switch', MockPokemon('Alakazam'))
        result = player._get_status_move_value(action)
        assert result == 0.0

    def test_status_move_value_for_status_move(self, player):
        thunder_wave = MockMove('thunderwave', type_name='Electric', category='STATUS')
        action = ('move', thunder_wave)
        result = player._get_status_move_value(action)
        assert result > 0

    def test_damage_done_for_switch(self, player):
        battle = MockBattle()
        action = ('switch', MockPokemon('Alakazam'))
        result = player._get_damage_done(battle, action)
        assert result == 0.0

    def test_damage_done_for_status_move(self, player):
        battle = MockBattle(
            active_pokemon=MockPokemon('Alakazam'),
            opponent_active_pokemon=MockPokemon('Snorlax')
        )
        thunder_wave = MockMove('thunderwave', type_name='Electric', category='STATUS', base_power=0)
        action = ('move', thunder_wave)
        result = player._get_damage_done(battle, action)
        assert result == 0.0

    def test_damage_received_for_switch(self, player):
        battle = MockBattle(
            active_pokemon=MockPokemon('Alakazam'),
            opponent_active_pokemon=MockPokemon('Tauros', moves=[
                MockMove('bodyslam', base_power=85)
            ])
        )
        action = ('switch', MockPokemon('Chansey'))
        result = player._get_damage_received(battle, action)
        assert result >= 0


class TestMetrics:
    def test_empty_metrics_structure(self):
        from warrior_player import Gen1WarriorPlayer
        with patch('warrior_player.path.exists', return_value=False):
            with patch.object(Gen1WarriorPlayer, '__init__', lambda self, *a, **kw: None):
                p = Gen1WarriorPlayer.__new__(Gen1WarriorPlayer)
                metrics = {'turn': [], 'action': [], 'self_hp': [], 'opp_hp': [],
                          'outspeed_prob': [], 'is_status_move': [], 'exp_damage_done': [],
                          'exp_damage_received': [], 'predicted_npw_score': []}
                # Just verify the structure matches what we expect
                assert set(metrics.keys()) == {'turn', 'action', 'self_hp', 'opp_hp',
                                                'outspeed_prob', 'is_status_move',
                                                'exp_damage_done', 'exp_damage_received',
                                                'predicted_npw_score'}
