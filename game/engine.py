# -----------------------------
# GAME ENGINE
# -----------------------------

import random

from game.clues.generators import room_clue, movement_clue, noise_clue, weapon_clue, random_clue, social_clue

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
def recall_player_memory(role, crime, guilty, innocent, weights):
    # Pick a clue type based on the role's weights
    clue_type = weighted_choice(weights)

    if clue_type == "incriminating":
        roll = random.random()
        # 25% chance to generate an incriminating clue of each type
        if roll < 0.25:
            return noise_clue(crime, 1)

        if 0.25 < roll < 0.50:
            return weapon_clue(crime, 1)

        if 0.50 < roll < 0.75:
            return room_clue(crime, 1)
        
        return movement_clue(crime, guilty, innocent, 1)

    if clue_type == "misleading":
        roll = random.random()
        # 25% chance to generate a misleading clue of each type
        if roll < 0.25:
            return noise_clue(crime, 0)

        if 0.25 < roll < 0.50:
            return weapon_clue(crime, 0)

        if 0.50 < roll < 0.75:
            return room_clue(crime, 0)
        
        return movement_clue(crime, guilty, innocent, 0)

    if clue_type == "social":
        return social_clue(guilty, innocent)

    return random_clue()


