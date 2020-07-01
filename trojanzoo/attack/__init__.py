# -*- coding: utf-8 -*-

from .attack import Attack
from .adv import *

class_dict = {
    'attack': 'Attack',

    'pgd': 'PGD',
    'inference': 'Inference',

    'poison': 'Poison',

    'badnet': 'BadNet',
    'trojannn': 'TrojanNN',
    'hidden_trigger': 'Hidden_Trigger',
    'latent_backdoor': 'Latent_Backdoor',

    'unify': 'Unify',
}
