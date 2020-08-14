#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Holds  dictionary objects for relevant game data.
"""

gen1_mons_dict = {
  'Abra': {
    'types': ['Psychic'],
    'bs': {'hp': 25, 'atk': 20, 'def': 15, 'spe': 90, 'spd': 105},
    'weightkg': 19.5,
    'nfe': True
  },
  'Aerodactyl': {
    'types': ['Rock', 'Flying'],
    'bs': {'hp': 80, 'atk': 105, 'def': 65, 'spe': 130, 'spd': 60},
    'weightkg': 59
  },
  'Alakazam': {
    'types': ['Psychic'],
    'bs': {'hp': 55, 'atk': 50, 'def': 45, 'spe': 120, 'spd': 135},
    'weightkg': 48
  },
  'Arbok': {
    'types': ['Poison'],
    'bs': {'hp': 60, 'atk': 85, 'def': 69, 'spe': 80, 'spd': 65},
    'weightkg': 65
  },
  'Arcanine': {
    'types': ['Fire'],
    'bs': {'hp': 90, 'atk': 110, 'def': 80, 'spe': 95, 'spd': 80},
    'weightkg': 155
  },
  'Articuno': {
    'types': ['Ice', 'Flying'],
    'bs': {'hp': 90, 'atk': 85, 'def': 100, 'spe': 85, 'spd': 125},
    'weightkg': 55.4
  },
  'Beedrill': {
    'types': ['Bug', 'Poison'],
    'bs': {'hp': 65, 'atk': 80, 'def': 40, 'spe': 75, 'spd': 45},
    'weightkg': 29.5
  },
  'Bellsprout': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 50, 'atk': 75, 'def': 35, 'spe': 40, 'spd': 70},
    'weightkg': 4,
    'nfe': True
  },
  'Blastoise': {
    'types': ['Water'],
    'bs': {'hp': 79, 'atk': 83, 'def': 100, 'spe': 78, 'spd': 85},
    'weightkg': 85.5
  },
  'Bulbasaur': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 45, 'atk': 49, 'def': 49, 'spe': 45, 'spd': 65},
    'weightkg': 6.9,
    'nfe': True
  },
  'Butterfree': {
    'types': ['Bug', 'Flying'],
    'bs': {'hp': 60, 'atk': 45, 'def': 50, 'spe': 70, 'spd': 80},
    'weightkg': 32
  },
  'Caterpie': {
    'types': ['Bug'],
    'bs': {'hp': 45, 'atk': 30, 'def': 35, 'spe': 45, 'spd': 20},
    'weightkg': 2.9,
    'nfe': True
  },
  'Chansey': {
    'types': ['Normal'],
    'bs': {'hp': 250, 'atk': 5, 'def': 5, 'spe': 50, 'spd': 105},
    'weightkg': 34.6
  },
  'Charizard': {
    'types': ['Fire', 'Flying'],
    'bs': {'hp': 78, 'atk': 84, 'def': 78, 'spe': 100, 'spd': 85},
    'weightkg': 90.5
  },
  'Charmander': {
    'types': ['Fire'],
    'bs': {'hp': 39, 'atk': 52, 'def': 43, 'spe': 65, 'spd': 50},
    'weightkg': 8.5,
    'nfe': True
  },
  'Charmeleon': {
    'types': ['Fire'],
    'bs': {'hp': 58, 'atk': 64, 'def': 58, 'spe': 80, 'spd': 65},
    'weightkg': 19,
    'nfe': True
  },
  'Clefable': {
    'types': ['Normal'],
    'bs': {'hp': 95, 'atk': 70, 'def': 73, 'spe': 60, 'spd': 85},
    'weightkg': 40
  },
  'Clefairy': {
    'types': ['Normal'],
    'bs': {'hp': 70, 'atk': 45, 'def': 48, 'spe': 35, 'spd': 60},
    'weightkg': 7.5,
    'nfe': True
  },
  'Cloyster': {
    'types': ['Water', 'Ice'],
    'bs': {'hp': 50, 'atk': 95, 'def': 180, 'spe': 70, 'spd': 85},
    'weightkg': 132.5
  },
  'Cubone': {
    'types': ['Ground'],
    'bs': {'hp': 50, 'atk': 50, 'def': 95, 'spe': 35, 'spd': 40},
    'weightkg': 6.5,
    'nfe': True
  },
  'Dewgong': {
    'types': ['Water', 'Ice'],
    'bs': {'hp': 90, 'atk': 70, 'def': 80, 'spe': 70, 'spd': 95},
    'weightkg': 120
  },
  'Diglett': {
    'types': ['Ground'],
    'bs': {'hp': 10, 'atk': 55, 'def': 25, 'spe': 95, 'spd': 45},
    'weightkg': 0.8,
    'nfe': True
  },
  'Ditto': {
    'types': ['Normal'],
    'bs': {'hp': 48, 'atk': 48, 'def': 48, 'spe': 48, 'spd': 48},
    'weightkg': 4
  },
  'Dodrio': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 60, 'atk': 110, 'def': 70, 'spe': 100, 'spd': 60},
    'weightkg': 85.2
  },
  'Doduo': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 35, 'atk': 85, 'def': 45, 'spe': 75, 'spd': 35},
    'weightkg': 39.2,
    'nfe': True
  },
  'Dragonair': {
    'types': ['Dragon'],
    'bs': {'hp': 61, 'atk': 84, 'def': 65, 'spe': 70, 'spd': 70},
    'weightkg': 16.5,
    'nfe': True
  },
  'Dragonite': {
    'types': ['Dragon', 'Flying'],
    'bs': {'hp': 91, 'atk': 134, 'def': 95, 'spe': 80, 'spd': 100},
    'weightkg': 210
  },
  'Dratini': {
    'types': ['Dragon'],
    'bs': {'hp': 41, 'atk': 64, 'def': 45, 'spe': 50, 'spd': 50},
    'weightkg': 3.3,
    'nfe': True
  },
  'Drowzee': {
    'types': ['Psychic'],
    'bs': {'hp': 60, 'atk': 48, 'def': 45, 'spe': 42, 'spd': 90},
    'weightkg': 32.4,
    'nfe': True
  },
  'Dugtrio': {
    'types': ['Ground'],
    'bs': {'hp': 35, 'atk': 80, 'def': 50, 'spe': 120, 'spd': 70},
    'weightkg': 33.3
  },
  'Eevee': {
    'types': ['Normal'],
    'bs': {'hp': 55, 'atk': 55, 'def': 50, 'spe': 55, 'spd': 65},
    'weightkg': 6.5,
    'nfe': True
  },
  'Ekans': {
    'types': ['Poison'],
    'bs': {'hp': 35, 'atk': 60, 'def': 44, 'spe': 55, 'spd': 40},
    'weightkg': 6.9,
    'nfe': True
  },
  'Electabuzz': {
    'types': ['Electric'],
    'bs': {'hp': 65, 'atk': 83, 'def': 57, 'spe': 105, 'spd': 85},
    'weightkg': 30
  },
  'Electrode': {
    'types': ['Electric'],
    'bs': {'hp': 60, 'atk': 50, 'def': 70, 'spe': 140, 'spd': 80},
    'weightkg': 66.6
  },
  'Exeggcute': {
    'types': ['Grass', 'Psychic'],
    'bs': {'hp': 60, 'atk': 40, 'def': 80, 'spe': 40, 'spd': 60},
    'weightkg': 2.5,
    'nfe': True
  },
  'Exeggutor': {
    'types': ['Grass', 'Psychic'],
    'bs': {'hp': 95, 'atk': 95, 'def': 85, 'spe': 55, 'spd': 125},
    'weightkg': 120
  },
  'Farfetch\u2019d': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 52, 'atk': 65, 'def': 55, 'spe': 60, 'spd': 58},
    'weightkg': 15
  },
  'Fearow': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 65, 'atk': 90, 'def': 65, 'spe': 100, 'spd': 61},
    'weightkg': 38
  },
  'Flareon': {
    'types': ['Fire'],
    'bs': {'hp': 65, 'atk': 130, 'def': 60, 'spe': 65, 'spd': 110},
    'weightkg': 25
  },
  'Gastly': {
    'types': ['Ghost', 'Poison'],
    'bs': {'hp': 30, 'atk': 35, 'def': 30, 'spe': 80, 'spd': 100},
    'weightkg': 0.1,
    'nfe': True
  },
  'Gengar': {
    'types': ['Ghost', 'Poison'],
    'bs': {'hp': 60, 'atk': 65, 'def': 60, 'spe': 110, 'spd': 130},
    'weightkg': 40.5
  },
  'Geodude': {
    'types': ['Rock', 'Ground'],
    'bs': {'hp': 40, 'atk': 80, 'def': 100, 'spe': 20, 'spd': 30},
    'weightkg': 20,
    'nfe': True
  },
  'Gloom': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 60, 'atk': 65, 'def': 70, 'spe': 40, 'spd': 85},
    'weightkg': 8.6,
    'nfe': True
  },
  'Golbat': {
    'types': ['Poison', 'Flying'],
    'bs': {'hp': 75, 'atk': 80, 'def': 70, 'spe': 90, 'spd': 75},
    'weightkg': 55
  },
  'Goldeen': {
    'types': ['Water'],
    'bs': {'hp': 45, 'atk': 67, 'def': 60, 'spe': 63, 'spd': 50},
    'weightkg': 15,
    'nfe': True
  },
  'Golduck': {
    'types': ['Water'],
    'bs': {'hp': 80, 'atk': 82, 'def': 78, 'spe': 85, 'spd': 80},
    'weightkg': 76.6
  },
  'Golem': {
    'types': ['Rock', 'Ground'],
    'bs': {'hp': 80, 'atk': 110, 'def': 130, 'spe': 45, 'spd': 55},
    'weightkg': 300
  },
  'Graveler': {
    'types': ['Rock', 'Ground'],
    'bs': {'hp': 55, 'atk': 95, 'def': 115, 'spe': 35, 'spd': 45},
    'weightkg': 105,
    'nfe': True
  },
  'Grimer': {
    'types': ['Poison'],
    'bs': {'hp': 80, 'atk': 80, 'def': 50, 'spe': 25, 'spd': 40},
    'weightkg': 30,
    'nfe': True
  },
  'Growlithe': {
    'types': ['Fire'],
    'bs': {'hp': 55, 'atk': 70, 'def': 45, 'spe': 60, 'spd': 50},
    'weightkg': 19,
    'nfe': True
  },
  'Gyarados': {
    'types': ['Water', 'Flying'],
    'bs': {'hp': 95, 'atk': 125, 'def': 79, 'spe': 81, 'spd': 100},
    'weightkg': 235
  },
  'Haunter': {
    'types': ['Ghost', 'Poison'],
    'bs': {'hp': 45, 'atk': 50, 'def': 45, 'spe': 95, 'spd': 115},
    'weightkg': 0.1,
    'nfe': True
  },
  'Hitmonchan': {
    'types': ['Fighting'],
    'bs': {'hp': 50, 'atk': 105, 'def': 79, 'spe': 76, 'spd': 35},
    'weightkg': 50.2
  },
  'Hitmonlee': {
    'types': ['Fighting'],
    'bs': {'hp': 50, 'atk': 120, 'def': 53, 'spe': 87, 'spd': 35},
    'weightkg': 49.8
  },
  'Horsea': {
    'types': ['Water'],
    'bs': {'hp': 30, 'atk': 40, 'def': 70, 'spe': 60, 'spd': 70},
    'weightkg': 8,
    'nfe': True
  },
  'Hypno': {
    'types': ['Psychic'],
    'bs': {'hp': 85, 'atk': 73, 'def': 70, 'spe': 67, 'spd': 115},
    'weightkg': 75.6
  },
  'Ivysaur': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 60, 'atk': 62, 'def': 63, 'spe': 60, 'spd': 80},
    'weightkg': 13,
    'nfe': True
  },
  'Jigglypuff': {
    'types': ['Normal'],
    'bs': {'hp': 115, 'atk': 45, 'def': 20, 'spe': 20, 'spd': 25},
    'weightkg': 5.5,
    'nfe': True
  },
  'Jolteon': {
    'types': ['Electric'],
    'bs': {'hp': 65, 'atk': 65, 'def': 60, 'spe': 130, 'spd': 110},
    'weightkg': 24.5
  },
  'Jynx': {
    'types': ['Ice', 'Psychic'],
    'bs': {'hp': 65, 'atk': 50, 'def': 35, 'spe': 95, 'spd': 95},
    'weightkg': 40.6
  },
  'Kabuto': {
    'types': ['Rock', 'Water'],
    'bs': {'hp': 30, 'atk': 80, 'def': 90, 'spe': 55, 'spd': 45},
    'weightkg': 11.5,
    'nfe': True
  },
  'Kabutops': {
    'types': ['Rock', 'Water'],
    'bs': {'hp': 60, 'atk': 115, 'def': 105, 'spe': 80, 'spd': 70},
    'weightkg': 40.5
  },
  'Kadabra': {
    'types': ['Psychic'],
    'bs': {'hp': 40, 'atk': 35, 'def': 30, 'spe': 105, 'spd': 120},
    'weightkg': 56.5,
    'nfe': True
  },
  'Kakuna': {
    'types': ['Bug', 'Poison'],
    'bs': {'hp': 45, 'atk': 25, 'def': 50, 'spe': 35, 'spd': 25},
    'weightkg': 10,
    'nfe': True
  },
  'Kangaskhan': {
    'types': ['Normal'],
    'bs': {'hp': 105, 'atk': 95, 'def': 80, 'spe': 90, 'spd': 40},
    'weightkg': 80
  },
  'Kingler': {
    'types': ['Water'],
    'bs': {'hp': 55, 'atk': 130, 'def': 115, 'spe': 75, 'spd': 50},
    'weightkg': 60
  },
  'Koffing': {
    'types': ['Poison'],
    'bs': {'hp': 40, 'atk': 65, 'def': 95, 'spe': 35, 'spd': 60},
    'weightkg': 1,
    'nfe': True
  },
  'Krabby': {
    'types': ['Water'],
    'bs': {'hp': 30, 'atk': 105, 'def': 90, 'spe': 50, 'spd': 25},
    'weightkg': 6.5,
    'nfe': True
  },
  'Lapras': {
    'types': ['Water', 'Ice'],
    'bs': {'hp': 130, 'atk': 85, 'def': 80, 'spe': 60, 'spd': 95},
    'weightkg': 220
  },
  'Lickitung': {
    'types': ['Normal'],
    'bs': {'hp': 90, 'atk': 55, 'def': 75, 'spe': 30, 'spd': 60},
    'weightkg': 65.5
  },
  'Machamp': {
    'types': ['Fighting'],
    'bs': {'hp': 90, 'atk': 130, 'def': 80, 'spe': 55, 'spd': 65},
    'weightkg': 130
  },
  'Machoke': {
    'types': ['Fighting'],
    'bs': {'hp': 80, 'atk': 100, 'def': 70, 'spe': 45, 'spd': 50},
    'weightkg': 70.5,
    'nfe': True
  },
  'Machop': {
    'types': ['Fighting'],
    'bs': {'hp': 70, 'atk': 80, 'def': 50, 'spe': 35, 'spd': 35},
    'weightkg': 19.5,
    'nfe': True
  },
  'Magikarp': {
    'types': ['Water'],
    'bs': {'hp': 20, 'atk': 10, 'def': 55, 'spe': 80, 'spd': 20},
    'weightkg': 10,
    'nfe': True
  },
  'Magmar': {
    'types': ['Fire'],
    'bs': {'hp': 65, 'atk': 95, 'def': 57, 'spe': 93, 'spd': 85},
    'weightkg': 44.5
  },
  'Magnemite': {
    'types': ['Electric'],
    'bs': {'hp': 25, 'atk': 35, 'def': 70, 'spe': 45, 'spd': 95},
    'weightkg': 6,
    'nfe': True
  },
  'Magneton': {
    'types': ['Electric'],
    'bs': {'hp': 50, 'atk': 60, 'def': 95, 'spe': 70, 'spd': 120},
    'weightkg': 60
  },
  'Mankey': {
    'types': ['Fighting'],
    'bs': {'hp': 40, 'atk': 80, 'def': 35, 'spe': 70, 'spd': 35},
    'weightkg': 28,
    'nfe': True
  },
  'Marowak': {
    'types': ['Ground'],
    'bs': {'hp': 60, 'atk': 80, 'def': 110, 'spe': 45, 'spd': 50},
    'weightkg': 45
  },
  'Meowth': {
    'types': ['Normal'],
    'bs': {'hp': 40, 'atk': 45, 'def': 35, 'spe': 90, 'spd': 40},
    'weightkg': 4.2,
    'nfe': True
  },
  'Metapod': {
    'types': ['Bug'],
    'bs': {'hp': 50, 'atk': 20, 'def': 55, 'spe': 30, 'spd': 25},
    'weightkg': 9.9,
    'nfe': True
  },
  'Mew': {
    'types': ['Psychic'],
    'bs': {'hp': 100, 'atk': 100, 'def': 100, 'spe': 100, 'spd': 100},
    'weightkg': 4
  },
  'Mewtwo': {
    'types': ['Psychic'],
    'bs': {'hp': 106, 'atk': 110, 'def': 90, 'spe': 130, 'spd': 154},
    'weightkg': 122
  },
  'Moltres': {
    'types': ['Fire', 'Flying'],
    'bs': {'hp': 90, 'atk': 100, 'def': 90, 'spe': 90, 'spd': 125},
    'weightkg': 60
  },
  'Mr. Mime': {
    'types': ['Psychic'],
    'bs': {'hp': 40, 'atk': 45, 'def': 65, 'spe': 90, 'spd': 100},
    'weightkg': 54.5
  },
  'Muk': {
    'types': ['Poison'],
    'bs': {'hp': 105, 'atk': 105, 'def': 75, 'spe': 50, 'spd': 65},
    'weightkg': 30
  },
  'Nidoking': {
    'types': ['Poison', 'Ground'],
    'bs': {'hp': 81, 'atk': 92, 'def': 77, 'spe': 85, 'spd': 75},
    'weightkg': 62
  },
  'Nidoqueen': {
    'types': ['Poison', 'Ground'],
    'bs': {'hp': 90, 'atk': 82, 'def': 87, 'spe': 76, 'spd': 75},
    'weightkg': 60
  },
  'Nidoran-F': {
    'types': ['Poison'],
    'bs': {'hp': 55, 'atk': 47, 'def': 52, 'spe': 41, 'spd': 40},
    'weightkg': 7,
    'nfe': True
  },
  'Nidoran-M': {
    'types': ['Poison'],
    'bs': {'hp': 46, 'atk': 57, 'def': 40, 'spe': 50, 'spd': 40},
    'weightkg': 9,
    'nfe': True
  },
  'Nidorina': {
    'types': ['Poison'],
    'bs': {'hp': 70, 'atk': 62, 'def': 67, 'spe': 56, 'spd': 55},
    'weightkg': 20,
    'nfe': True
  },
  'Nidorino': {
    'types': ['Poison'],
    'bs': {'hp': 61, 'atk': 72, 'def': 57, 'spe': 65, 'spd': 55},
    'weightkg': 19.5,
    'nfe': True
  },
  'Ninetales': {
    'types': ['Fire'],
    'bs': {'hp': 73, 'atk': 76, 'def': 75, 'spe': 100, 'spd': 100},
    'weightkg': 19.9
  },
  'Oddish': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 45, 'atk': 50, 'def': 55, 'spe': 30, 'spd': 75},
    'weightkg': 5.4,
    'nfe': True
  },
  'Omanyte': {
    'types': ['Rock', 'Water'],
    'bs': {'hp': 35, 'atk': 40, 'def': 100, 'spe': 35, 'spd': 90},
    'weightkg': 7.5,
    'nfe': True
  },
  'Omastar': {
    'types': ['Rock', 'Water'],
    'bs': {'hp': 70, 'atk': 60, 'def': 125, 'spe': 55, 'spd': 115},
    'weightkg': 35
  },
  'Onix': {
    'types': ['Rock', 'Ground'],
    'bs': {'hp': 35, 'atk': 45, 'def': 160, 'spe': 70, 'spd': 30},
    'weightkg': 210
  },
  'Paras': {
    'types': ['Bug', 'Grass'],
    'bs': {'hp': 35, 'atk': 70, 'def': 55, 'spe': 25, 'spd': 55},
    'weightkg': 5.4,
    'nfe': True
  },
  'Parasect': {
    'types': ['Bug', 'Grass'],
    'bs': {'hp': 60, 'atk': 95, 'def': 80, 'spe': 30, 'spd': 80},
    'weightkg': 29.5
  },
  'Persian': {
    'types': ['Normal'],
    'bs': {'hp': 65, 'atk': 70, 'def': 60, 'spe': 115, 'spd': 65},
    'weightkg': 32
  },
  'Pidgeot': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 83, 'atk': 80, 'def': 75, 'spe': 91, 'spd': 70},
    'weightkg': 39.5
  },
  'Pidgeotto': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 63, 'atk': 60, 'def': 55, 'spe': 71, 'spd': 50},
    'weightkg': 30,
    'nfe': True
  },
  'Pidgey': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 40, 'atk': 45, 'def': 40, 'spe': 56, 'spd': 35},
    'weightkg': 1.8,
    'nfe': True
  },
  'Pikachu': {
    'types': ['Electric'],
    'bs': {'hp': 35, 'atk': 55, 'def': 30, 'spe': 90, 'spd': 50},
    'weightkg': 6,
    'nfe': True
  },
  'Pinsir': {
    'types': ['Bug'],
    'bs': {'hp': 65, 'atk': 125, 'def': 100, 'spe': 85, 'spd': 55},
    'weightkg': 55
  },
  'Poliwag': {
    'types': ['Water'],
    'bs': {'hp': 40, 'atk': 50, 'def': 40, 'spe': 90, 'spd': 40},
    'weightkg': 12.4,
    'nfe': True
  },
  'Poliwhirl': {
    'types': ['Water'],
    'bs': {'hp': 65, 'atk': 65, 'def': 65, 'spe': 90, 'spd': 50},
    'weightkg': 20,
    'nfe': True
  },
  'Poliwrath': {
    'types': ['Water', 'Fighting'],
    'bs': {'hp': 90, 'atk': 85, 'def': 95, 'spe': 70, 'spd': 70},
    'weightkg': 54
  },
  'Ponyta': {
    'types': ['Fire'],
    'bs': {'hp': 50, 'atk': 85, 'def': 55, 'spe': 90, 'spd': 65},
    'weightkg': 30,
    'nfe': True
  },
  'Porygon': {
    'types': ['Normal'],
    'bs': {'hp': 65, 'atk': 60, 'def': 70, 'spe': 40, 'spd': 75},
    'weightkg': 36.5
  },
  'Primeape': {
    'types': ['Fighting'],
    'bs': {'hp': 65, 'atk': 105, 'def': 60, 'spe': 95, 'spd': 60},
    'weightkg': 32
  },
  'Psyduck': {
    'types': ['Water'],
    'bs': {'hp': 50, 'atk': 52, 'def': 48, 'spe': 55, 'spd': 50},
    'weightkg': 19.6,
    'nfe': True
  },
  'Raichu': {
    'types': ['Electric'],
    'bs': {'hp': 60, 'atk': 90, 'def': 55, 'spe': 100, 'spd': 90},
    'weightkg': 30
  },
  'Rapidash': {
    'types': ['Fire'],
    'bs': {'hp': 65, 'atk': 100, 'def': 70, 'spe': 105, 'spd': 80},
    'weightkg': 95
  },
  'Raticate': {
    'types': ['Normal'],
    'bs': {'hp': 55, 'atk': 81, 'def': 60, 'spe': 97, 'spd': 50},
    'weightkg': 18.5
  },
  'Rattata': {
    'types': ['Normal'],
    'bs': {'hp': 30, 'atk': 56, 'def': 35, 'spe': 72, 'spd': 25},
    'weightkg': 3.5,
    'nfe': True
  },
  'Rhydon': {
    'types': ['Ground', 'Rock'],
    'bs': {'hp': 105, 'atk': 130, 'def': 120, 'spe': 40, 'spd': 45},
    'weightkg': 120
  },
  'Rhyhorn': {
    'types': ['Ground', 'Rock'],
    'bs': {'hp': 80, 'atk': 85, 'def': 95, 'spe': 25, 'spd': 30},
    'weightkg': 115,
    'nfe': True
  },
  'Sandshrew': {
    'types': ['Ground'],
    'bs': {'hp': 50, 'atk': 75, 'def': 85, 'spe': 40, 'spd': 30},
    'weightkg': 12,
    'nfe': True
  },
  'Sandslash': {
    'types': ['Ground'],
    'bs': {'hp': 75, 'atk': 100, 'def': 110, 'spe': 65, 'spd': 55},
    'weightkg': 29.5
  },
  'Scyther': {
    'types': ['Bug', 'Flying'],
    'bs': {'hp': 70, 'atk': 110, 'def': 80, 'spe': 105, 'spd': 55},
    'weightkg': 56
  },
  'Seadra': {
    'types': ['Water'],
    'bs': {'hp': 55, 'atk': 65, 'def': 95, 'spe': 85, 'spd': 95},
    'weightkg': 25
  },
  'Seaking': {
    'types': ['Water'],
    'bs': {'hp': 80, 'atk': 92, 'def': 65, 'spe': 68, 'spd': 80},
    'weightkg': 39
  },
  'Seel': {
    'types': ['Water'],
    'bs': {'hp': 65, 'atk': 45, 'def': 55, 'spe': 45, 'spd': 70},
    'weightkg': 90,
    'nfe': True
  },
  'Shellder': {
    'types': ['Water'],
    'bs': {'hp': 30, 'atk': 65, 'def': 100, 'spe': 40, 'spd': 45},
    'weightkg': 4,
    'nfe': True
  },
  'Slowbro': {
    'types': ['Water', 'Psychic'],
    'bs': {'hp': 95, 'atk': 75, 'def': 110, 'spe': 30, 'spd': 80},
    'weightkg': 78.5
  },
  'Slowpoke': {
    'types': ['Water', 'Psychic'],
    'bs': {'hp': 90, 'atk': 65, 'def': 65, 'spe': 15, 'spd': 40},
    'weightkg': 36,
    'nfe': True
  },
  'Snorlax': {
    'types': ['Normal'],
    'bs': {'hp': 160, 'atk': 110, 'def': 65, 'spe': 30, 'spd': 65},
    'weightkg': 460
  },
  'Spearow': {
    'types': ['Normal', 'Flying'],
    'bs': {'hp': 40, 'atk': 60, 'def': 30, 'spe': 70, 'spd': 31},
    'weightkg': 2,
    'nfe': True
  },
  'Squirtle': {
    'types': ['Water'],
    'bs': {'hp': 44, 'atk': 48, 'def': 65, 'spe': 43, 'spd': 50},
    'weightkg': 9,
    'nfe': True
  },
  'Starmie': {
    'types': ['Water', 'Psychic'],
    'bs': {'hp': 60, 'atk': 75, 'def': 85, 'spe': 115, 'spd': 100},
    'weightkg': 80
  },
  'Staryu': {
    'types': ['Water'],
    'bs': {'hp': 30, 'atk': 45, 'def': 55, 'spe': 85, 'spd': 70},
    'weightkg': 34.5,
    'nfe': True
  },
  'Tangela': {
    'types': ['Grass'],
    'bs': {'hp': 65, 'atk': 55, 'def': 115, 'spe': 60, 'spd': 100},
    'weightkg': 35
  },
  'Tauros': {
    'types': ['Normal'],
    'bs': {'hp': 75, 'atk': 100, 'def': 95, 'spe': 110, 'spd': 70},
    'weightkg': 88.4
  },
  'Tentacool': {
    'types': ['Water', 'Poison'],
    'bs': {'hp': 40, 'atk': 40, 'def': 35, 'spe': 70, 'spd': 100},
    'weightkg': 45.5,
    'nfe': True
  },
  'Tentacruel': {
    'types': ['Water', 'Poison'],
    'bs': {'hp': 80, 'atk': 70, 'def': 65, 'spe': 100, 'spd': 120},
    'weightkg': 55
  },
  'Vaporeon': {
    'types': ['Water'],
    'bs': {'hp': 130, 'atk': 65, 'def': 60, 'spe': 65, 'spd': 110},
    'weightkg': 29
  },
  'Venomoth': {
    'types': ['Bug', 'Poison'],
    'bs': {'hp': 70, 'atk': 65, 'def': 60, 'spe': 90, 'spd': 90},
    'weightkg': 12.5
  },
  'Venonat': {
    'types': ['Bug', 'Poison'],
    'bs': {'hp': 60, 'atk': 55, 'def': 50, 'spe': 45, 'spd': 40},
    'weightkg': 30,
    'nfe': True
  },
  'Venusaur': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 80, 'atk': 82, 'def': 83, 'spe': 80, 'spd': 100},
    'weightkg': 100
  },
  'Victreebel': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 80, 'atk': 105, 'def': 65, 'spe': 70, 'spd': 100},
    'weightkg': 15.5
  },
  'Vileplume': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 75, 'atk': 80, 'def': 85, 'spe': 50, 'spd': 100},
    'weightkg': 18.6
  },
  'Voltorb': {
    'types': ['Electric'],
    'bs': {'hp': 40, 'atk': 30, 'def': 50, 'spe': 100, 'spd': 55},
    'weightkg': 10.4,
    'nfe': True
  },
  'Vulpix': {
    'types': ['Fire'],
    'bs': {'hp': 38, 'atk': 41, 'def': 40, 'spe': 65, 'spd': 65},
    'weightkg': 9.9,
    'nfe': True
  },
  'Wartortle': {
    'types': ['Water'],
    'bs': {'hp': 59, 'atk': 63, 'def': 80, 'spe': 58, 'spd': 65},
    'weightkg': 22.5,
    'nfe': True
  },
  'Weedle': {
    'types': ['Bug', 'Poison'],
    'bs': {'hp': 40, 'atk': 35, 'def': 30, 'spe': 50, 'spd': 20},
    'weightkg': 3.2,
    'nfe': True
  },
  'Weepinbell': {
    'types': ['Grass', 'Poison'],
    'bs': {'hp': 65, 'atk': 90, 'def': 50, 'spe': 55, 'spd': 85},
    'weightkg': 6.4,
    'nfe': True
  },
  'Weezing': {
    'types': ['Poison'],
    'bs': {'hp': 65, 'atk': 90, 'def': 120, 'spe': 60, 'spd': 85},
    'weightkg': 9.5
  },
  'Wigglytuff': {
    'types': ['Normal'],
    'bs': {'hp': 140, 'atk': 70, 'def': 45, 'spe': 45, 'spd': 50},
    'weightkg': 12
  },
  'Zapdos': {
    'types': ['Electric', 'Flying'],
    'bs': {'hp': 90, 'atk': 90, 'def': 85, 'spe': 100, 'spd': 125},
    'weightkg': 52.6
  },
  'Zubat': {
    'types': ['Poison', 'Flying'],
    'bs': {'hp': 40, 'atk': 45, 'def': 35, 'spe': 55, 'spd': 40},
    'weightkg': 7.5,
    'nfe': True
  }
}

gen1_moves_dict = {
  '(No Move)': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Recharge': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Absorb': {'bp': 20, 'type': 'Grass', 'drain': [1, 2], 'accuracy':100},
  'Acid': {'bp': 40, 'type': 'Poison', 'accuracy':100},
  'Amnesia': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Aurora Beam': {'bp': 65, 'type': 'Ice', 'accuracy':100},
  'Barrage': {'bp': 15, 'type': 'Normal', 'multihit': [2, 5], 'accuracy':85},
  'Bide': {'bp': 0, 'type': '???'},
  'Bind': {'bp': 15, 'type': 'Normal', 'accuracy':85},
  'Bite': {'bp': 60, 'type': 'Normal', 'accuracy':100},
  'Blizzard': {'bp': 120, 'type': 'Ice', 'accuracy':90, 'statusperc':10},
  'Bonemerang': {'bp': 50, 'type': 'Ground', 'multihit': 2, 'accuracy':90},
  'Bubble': {'bp': 20, 'type': 'Water', 'accuracy':100},
  'Bubble Beam': {'bp': 65, 'type': 'Water', 'accuracy':100},
  'Clamp': {'bp': 35, 'type': 'Water', 'accuracy':85},
  'Comet Punch': {'bp': 18, 'type': 'Normal', 'multihit': [2, 5], 'accuracy':85},
  'Constrict': {'bp': 10, 'type': 'Normal'},
  'Conversion': {'bp': 0, 'category': 'Status', 'type': 'Normal', },
  'Counter': {'bp': 0, 'type': 'Fighting', 'accuracy':100},
  'Crabhammer': {'bp': 90, 'type': 'Water', 'accuracy':90},
  'Defense Curl': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Dig': {'bp': 100, 'type': 'Ground', 'accuracy':100},
  'Disable': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Dizzy Punch': {'bp': 70, 'type': 'Normal', 'accuracy':100},
  'Double-Edge': {'bp': 100, 'type': 'Normal', 'recoil': [25, 100], 'accuracy':100},
  'Double Kick': {'bp': 30, 'type': 'Fighting', 'multihit': 2, 'accuracy':100},
  'Double Slap': {'bp': 15, 'type': 'Normal', 'multihit': [2, 5], 'accuracy':100},
  'Dragon Rage': {'bp': 1, 'type': 'Dragon', 'accuracy':100},
  'Dream Eater': {'bp': 100, 'type': 'Psychic', 'drain': [1, 2], 'accuracy':100},
  'Earthquake': {'bp': 100, 'type': 'Ground', 'accuracy':100},
  'Explosion': {'bp': 170, 'type': 'Normal', 'accuracy':100},
  'Fire Blast': {'bp': 120, 'type': 'Fire', 'accuracy':85, 'statusperc':30},
  'Fire Spin': {'bp': 15, 'type': 'Fire', 'accuracy':85},
  'Fissure': {'bp': 0, 'type': 'Ground', 'accuracy':30},
  'Fly': {'bp': 70, 'type': 'Flying', 'accuracy':95},
  'Focus Energy': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Fury Attack': {'bp': 15, 'type': 'Normal', 'multihit': [2, 5], 'accuracy':85},
  'Fury Swipes': {'bp': 18, 'type': 'Normal', 'multihit': [2, 5], 'accuracy':80},
  'Glare': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Growth': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Guillotine': {'bp': 0, 'type': 'Normal', 'accuracy':30},
  'Gust': {'bp': 40, 'type': 'Normal', 'accuracy':100},
  'Haze': {'bp': 0, 'category': 'Status', 'type': 'Ice'},
  'High Jump Kick': {'bp': 85, 'type': 'Fighting', 'hasCrashDamage': True, 'accuracy':90},
  'Horn Drill': {'bp': 0, 'type': 'Normal', 'accuracy':30},
  'Hyper Beam': {'bp': 150, 'type': 'Normal', 'accuracy':90},
  'Jump Kick': {'bp': 70, 'type': 'Fighting', 'hasCrashDamage': True, 'accuracy':95},
  'Karate Chop': {'bp': 50, 'type': 'Normal', 'accuracy':100},
  'Leech Seed': {'bp': 0, 'category': 'Status', 'type': 'Grass', 'accuracy':90},
  'Light Screen': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Metronome': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Mimic': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Minimize': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Mirror Move': {'bp': 0, 'category': 'Status', 'type': 'Flying'},
  'Mist': {'bp': 0, 'category': 'Status', 'type': 'Ice'},
  'Night Shade': {'bp': 1, 'type': 'Ghost', 'accuracy':100},
  'Petal Dance': {'bp': 70, 'type': 'Grass', 'accuracy':100},
  'Pin Missile': {'bp': 14, 'type': 'Bug', 'multihit': [2, 5], 'accuracy':95},
  'Poison Sting': {'bp': 15, 'type': 'Poison', 'accuracy':100, 'statusperc':20},
  'Psychic': {'bp': 90, 'type': 'Psychic', 'accuracy':100},
  'Psywave': {'bp': 1, 'type': 'Psychic', 'accuracy':100},
  'Rage': {'bp': 20, 'type': 'Normal', 'accuracy':100},
  'Razor Leaf': {'bp': 55, 'type': 'Grass', 'accuracy':95},
  'Razor Wind': {'bp': 80, 'type': 'Normal', 'accuracy':100},
  'Recover': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Reflect': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Rest': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Roar': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Rock Slide': {'bp': 75, 'type': 'Rock', 'accuracy':90},
  'Rock Throw': {'bp': 50, 'type': 'Rock', 'accuracy':90},
  'Sand Attack': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Seismic Toss': {'bp': 1, 'type': 'Fighting', 'accuracy':100},
  'Self-Destruct': {'bp': 130, 'type': 'Normal', 'accuracy':100},
  'Skull Bash': {'bp': 100, 'type': 'Normal', 'accuracy':100},
  'Slash': {'bp': 70, 'type': 'Normal', 'accuracy':100},
  'Sludge': {'bp': 65, 'type': 'Poison', 'accuracy':100, 'statusperc':40},
  'Soft-Boiled': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Solar Beam': {'bp': 120, 'type': 'Grass', 'accuracy':100},
  'Sonic Boom': {'bp': 0, 'type': 'Normal', 'accuracy':90},
  'Spike Cannon': {'bp': 20, 'type': 'Normal', 'multihit': [2, 5], 'accuracy':100},
  'Stomp': {'bp': 65, 'type': 'Normal', 'accuracy':100},
  'Struggle': {'bp': 50, 'type': 'Normal', 'recoil': [1, 2]},
  'Stun Spore': {'bp': 0, 'category': 'Status', 'type': 'Grass', 'accuracy':75},
  'Submission': {'bp': 80, 'type': 'Fighting', 'recoil': [1, 4], 'accuracy':80},
  'Substitute': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Super Fang': {'bp': 1, 'type': 'Normal', 'accuracy':90},
  'Swift': {'bp': 60, 'type': 'Normal'},
  'Take Down': {'bp': 90, 'type': 'Normal', 'recoil': [1, 4], 'accuracy':85},
  'Thrash': {'bp': 90, 'type': 'Normal', 'accuracy':100},
  'Thunder': {'bp': 120, 'type': 'Electric', 'accuracy':70, 'statusperc':10},
  'Thunder Wave': {'bp': 0, 'category': 'Status', 'type': 'Electric', 'accuracy':90},
  'Transform': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Tri Attack': {'bp': 80, 'type': 'Normal', 'accuracy':100},
  'Twineedle': {'bp': 25, 'type': 'Bug', 'multihit': 2, 'accuracy':100},
  'Whirlwind': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Wing Attack': {'bp': 35, 'type': 'Flying', 'accuracy':100},
  'Wrap': {'bp': 15, 'type': 'Normal','accuracy':90},
  'Growl': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Leer': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Low Kick': {'bp': 50, 'type': 'Fighting', 'accuracy':100},
  'Poison Gas': {'bp': 0, 'category': 'Status', 'type': 'Poison', 'accuracy':90},
  'Poison Powder': {'bp': 0, 'category': 'Status', 'type': 'Poison', 'accuracy':75},
  'Sky Attack': {'bp': 140, 'type': 'Flying', 'accuracy':90},
  'String Shot': {'bp': 0, 'category': 'Status', 'type': 'Bug', 'accuracy':95},
  'Surf': {'bp': 95, 'type': 'Water', 'accuracy':100},
  'Tail Whip': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Toxic': {'bp': 0, 'category': 'Status', 'type': 'Poison', 'accuracy':90},
  'Flash': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Hypnosis': {'bp': 0, 'category': 'Status', 'type': 'Psychic', 'accuracy':60},
  'Leech Life': {'bp': 20, 'type': 'Bug', 'drain': [1, 2], 'accuracy':100},
  'Mega Drain': {'bp': 40, 'type': 'Grass', 'drain': [1, 2], 'accuracy':100},
  'Vine Whip': {'bp': 35, 'type': 'Grass', 'accuracy':100},
  'Waterfall': {'bp': 80, 'type': 'Water','accuracy':100},
  'Tackle': {'bp': 35, 'type': 'Normal', 'accuracy':100},
  'Acid Armor': {'bp': 0, 'category': 'Status', 'type': 'Poison'},
  'Barrier': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Body Slam': {'bp': 85, 'type': 'Normal', 'accuracy':100, 'statusperc':30},
  'Flamethrower': {'bp': 95, 'type': 'Fire', 'accuracy':100, 'statusperc':10},
  'Hydro Pump': {'bp': 120, 'type': 'Water', 'accuracy':80},
  'Ice Beam': {'bp': 95, 'type': 'Ice', 'accuracy':100, 'statusperc':10},
  'Lick': {'bp': 20, 'type': 'Ghost', 'accuracy':100, 'statusperc':30},
  'Screech': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':85},
  'Sing': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':55},
  'Sleep Powder': {'bp': 0, 'category': 'Status', 'type': 'Grass', 'accuracy':75},
  'Smog': {'bp': 20, 'type': 'Poison', 'accuracy':100, 'statusperc':40},
  'Spore': {'bp': 0, 'category': 'Status', 'type': 'Grass', 'accuracy':100},
  'Supersonic': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':55},
  'Swords Dance': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Thunderbolt': {'bp': 95, 'type': 'Electric', 'accuracy':100, 'statusperc':10},
  'Bone Club': {'bp': 65, 'type': 'Ground', 'accuracy':85},
  'Egg Bomb': {'bp': 100, 'type': 'Normal', 'accuracy':75},
  'Hyper Fang': {'bp': 80, 'type': 'Normal', 'accuracy':90},
  'Kinesis': {'bp': 0, 'category': 'Status', 'type': 'Psychic', 'accuracy':80},
  'Lovely Kiss': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':75},
  'Meditate': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Rolling Kick': {'bp': 60, 'type': 'Fighting', 'accuracy':85},
  'Sharpen': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Teleport': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Agility': {'bp': 0, 'category': 'Status', 'type': 'Psychic'},
  'Confuse Ray': {'bp': 0, 'category': 'Status', 'type': 'Ghost', 'accuracy':100},
  'Confusion': {'bp': 50, 'type': 'Psychic', 'accuracy':100},
  'Cut': {'bp': 50, 'type': 'Normal', 'accuracy':95},
  'Double Team': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Drill Peck': {'bp': 80, 'type': 'Flying', 'accuracy':100},
  'Ember': {'bp': 40, 'type': 'Fire', 'accuracy':100, 'statusperc':10},
  'Fire Punch': {'bp': 75, 'type': 'Fire', 'accuracy':100, 'statusperc':10},
  'Harden': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Headbutt': {'bp': 70, 'type': 'Normal', 'accuracy':100},
  'Horn Attack': {'bp': 65, 'type': 'Normal', 'accuracy':100},
  'Ice Punch': {'bp': 75, 'type': 'Ice', 'accuracy':100, 'statusperc':10},
  'Mega Kick': {'bp': 120, 'type': 'Normal', 'accuracy':75},
  'Mega Punch': {'bp': 80, 'type': 'Normal', 'accuracy':85},
  'Paleo Wave': {'bp': 85, 'type': 'Rock'},
  'Pay Day': {'bp': 40, 'type': 'Normal', 'accuracy':100},
  'Peck': {'bp': 35, 'type': 'Flying', 'accuracy':100},
  'Pound': {'bp': 40, 'type': 'Normal', 'accuracy':100},
  'Psybeam': {'bp': 65, 'type': 'Psychic', 'accuracy':100, 'statusperc':10},
  'Quick Attack': {'bp': 40, 'type': 'Normal', 'priority': 1, 'accuracy':100},
  'Scratch': {'bp': 40, 'type': 'Normal', 'accuracy':100},
  'Shadow Strike': {'bp': 80, 'type': 'Ghost'},
  'Slam': {'bp': 80, 'type': 'Normal', 'accuracy':75},
  'Smokescreen': {'bp': 0, 'category': 'Status', 'type': 'Normal', 'accuracy':100},
  'Splash': {'bp': 0, 'category': 'Status', 'type': 'Normal'},
  'Strength': {'bp': 80, 'type': 'Normal', 'accuracy':100},
  'Thunder Punch': {'bp': 75, 'type': 'Electric', 'accuracy':100, 'statusperc':10},
  'Thunder Shock': {'bp': 40, 'type': 'Electric', 'accuracy':100, 'statusperc':10},
  'Vise Grip': {'bp': 55, 'type': 'Normal','accuracy':100},
  'Water Gun': {'bp': 40, 'type': 'Water','accuracy':100},
  'Withdraw': {'bp': 0, 'category': 'Status', 'type': 'Water'}
}

type_effectiveness_dict = {
  '???': {
    'Normal': 1,
    'Grass': 1,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 1,
    'Poison': 1,
    'Ground': 1,
    'Rock': 1,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 1,
  },
  'Normal': {
    '???': 1,
    'Normal': 1,
    'Grass': 1,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 1,
    'Poison': 1,
    'Ground': 1,
    'Rock': 0.5,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 0,
    'Dragon': 1,
  },
  'Grass': {
    '???': 1,
    'Normal': 1,
    'Grass': 0.5,
    'Fire': 0.5,
    'Water': 2,
    'Electric': 1,
    'Ice': 1,
    'Flying': 0.5,
    'Bug': 0.5,
    'Poison': 0.5,
    'Ground': 2,
    'Rock': 2,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 0.5,
  },
  'Fire': {
    '???': 1,
    'Normal': 1,
    'Grass': 2,
    'Fire': 0.5,
    'Water': 0.5,
    'Electric': 1,
    'Ice': 2,
    'Flying': 1,
    'Bug': 2,
    'Poison': 1,
    'Ground': 1,
    'Rock': 0.5,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 0.5,
  },
  'Water': {
    '???': 1,
    'Normal': 1,
    'Grass': 0.5,
    'Fire': 2,
    'Water': 0.5,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 1,
    'Poison': 1,
    'Ground': 2,
    'Rock': 2,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 0.5,
  },
  'Electric': {
    '???': 1,
    'Normal': 1,
    'Grass': 0.5,
    'Fire': 1,
    'Water': 2,
    'Electric': 0.5,
    'Ice': 1,
    'Flying': 2,
    'Bug': 1,
    'Poison': 1,
    'Ground': 0,
    'Rock': 1,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 0.5,
  },
  'Ice': {
    '???': 1,
    'Normal': 1,
    'Grass': 2,
    'Fire': 1,
    'Water': 0.5,
    'Electric': 1,
    'Ice': 0.5,
    'Flying': 2,
    'Bug': 1,
    'Poison': 1,
    'Ground': 2,
    'Rock': 1,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 2,
  },
  'Flying': {
    '???': 1,
    'Normal': 1,
    'Grass': 2,
    'Fire': 1,
    'Water': 1,
    'Electric': 0.5,
    'Ice': 1,
    'Flying': 1,
    'Bug': 2,
    'Poison': 1,
    'Ground': 1,
    'Rock': 0.5,
    'Fighting': 2,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 1,
  },
  'Bug': {
    '???': 1,
    'Normal': 1,
    'Grass': 2,
    'Fire': 0.5,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 0.5,
    'Bug': 1,
    'Poison': 2,
    'Ground': 1,
    'Rock': 1,
    'Fighting': 0.5,
    'Psychic': 2,
    'Ghost': 0.5,
    'Dragon': 1,
  },
  'Poison': {
    '???': 1,
    'Normal': 1,
    'Grass': 2,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 2,
    'Poison': 0.5,
    'Ground': 0.5,
    'Rock': 0.5,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 0.5,
    'Dragon': 1,
  },
  'Ground': {
    '???': 1,
    'Normal': 1,
    'Grass': 0.5,
    'Fire': 2,
    'Water': 1,
    'Electric': 2,
    'Ice': 1,
    'Flying': 0,
    'Bug': 0.5,
    'Poison': 2,
    'Ground': 1,
    'Rock': 2,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 1,
  },
  'Rock': {
    '???': 1,
    'Normal': 1,
    'Grass': 1,
    'Fire': 2,
    'Water': 1,
    'Electric': 1,
    'Ice': 2,
    'Flying': 2,
    'Bug': 2,
    'Poison': 1,
    'Ground': 0.5,
    'Rock': 1,
    'Fighting': 0.5,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 1,
  },
  'Fighting': {
    '???': 1,
    'Normal': 2,
    'Grass': 1,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 2,
    'Flying': 0.5,
    'Bug': 0.5,
    'Poison': 0.5,
    'Ground': 1,
    'Rock': 2,
    'Fighting': 1,
    'Psychic': 0.5,
    'Ghost': 0,
    'Dragon': 1,
  },
  'Psychic': {
    '???': 1,
    'Normal': 1,
    'Grass': 1,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 1,
    'Poison': 2,
    'Ground': 1,
    'Rock': 1,
    'Fighting': 2,
    'Psychic': 0.5,
    'Ghost': 1,
    'Dragon': 1,
  },
  'Ghost': {
    '???': 1,
    'Normal': 0,
    'Grass': 1,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 1,
    'Poison': 1,
    'Ground': 1,
    'Rock': 1,
    'Fighting': 1,
    'Psychic': 0,
    'Ghost': 2,
    'Dragon': 1,
  },
  'Dragon': {
    '???': 1,
    'Normal': 1,
    'Grass': 1,
    'Fire': 1,
    'Water': 1,
    'Electric': 1,
    'Ice': 1,
    'Flying': 1,
    'Bug': 1,
    'Poison': 1,
    'Ground': 1,
    'Rock': 1,
    'Fighting': 1,
    'Psychic': 1,
    'Ghost': 1,
    'Dragon': 2,
  }
}
