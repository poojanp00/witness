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
def recall_player_memory(crime, guilty, innocent, lovers, weights):
    # Pick a clue type based on the role's weights
    clue_type = weighted_choice(weights)

    if clue_type == "incriminating":
        clue_options = [
            lambda: noise_clue(crime, 1),
            lambda: weapon_clue(crime, 1),
            lambda: room_clue(crime, 1),
            lambda: movement_clue(crime, guilty, innocent, 1)
        ]
        # Randomly select and execute one
        return random.choice(clue_options)()

    if clue_type == "misleading":
        clue_options = [
            lambda: noise_clue(crime, 0),
            lambda: weapon_clue(crime, 0),
            lambda: room_clue(crime, 0),
            lambda: movement_clue(crime, guilty, innocent, 0)
        ]
        # Randomly select and execute one
        return random.choice(clue_options)()

    if clue_type == "social":
        roll = random.random()
        if roll < 0.4 :
            return social_clue(guilty)
        if 0.4 < roll < 0.8:
            return social_clue(lovers) 
        else:
            innocent_pair = random.sample(innocent, 2) # all guests
            return social_clue(innocent_pair)

    return random_clue()


