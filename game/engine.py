# -----------------------------
# GAME ENGINE
# -----------------------------


import random

# from game.data.weapon import weapons
# from game.data.room import rooms

# from game.utils.time_utils import random_time
from game.clues.noise import noise_clue
from game.clues.movement import movement_clue
from game.clues.room import room_clue
from game.clues.weapon import weapon_clue
from game.clues.random import random_clue, social_clue

from game.weights import weights

# -----------------------------
# CLUE TYPE PICKER
# -----------------------------
# This function takes a role's weights dictionary, and returns a clue type
# ------------------------------
def weighted_choice(weight_dict):
    total = sum(weight_dict.values())
    r = random.uniform(0,total)
    upto = 0
    for k,v in weight_dict.items():
        if upto+v >= r:
            return k
        upto += v


# -----------------------------
# CLUE FACTORY
# -----------------------------
# This function takes a role and a crime, and generates a clue based on the role's weights.
# The clue can be incriminating, misleading, social, or random.
# -----------------------------

def generate_clue(role, crime):
    # Pick a clue type based on the role's weights
    clue_type = weighted_choice(weights[role])

    if clue_type == "incriminating":
        roll = random.random()
        # 25% chance to generate an incriminating clue of each type
        if roll < 0.25:
            return noise_clue(crime, 1)

        if 0.25 < roll < 0.50:
            return weapon_clue(crime, 1)

        if 0.50 < roll < 0.75:
            return room_clue(crime, 1)
        
        return movement_clue(crime, 1)

    if clue_type == "misleading":
        roll = random.random()
        # 25% chance to generate a misleading clue of each type
        if roll < 0.25:
            return noise_clue(crime, 0)

        if 0.25 < roll < 0.50:
            return weapon_clue(crime, 0)

        if 0.50 < roll < 0.75:
            return room_clue(crime, 0)
        
        return movement_clue(crime, 0)

    if clue_type == "social":
        return social_clue()

    return random_clue()


