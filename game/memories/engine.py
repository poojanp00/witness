# -----------------------------
# GAME ENGINE
# -----------------------------

import random

from game.memories.generators import room_memory, movement_memory, weapon_noise_memory, weapon_evidence_memory, random_memory, social_memory

# -----------------------------
# MEMORY TYPE PICKER
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
# MEMORY FACTORY
# -----------------------------
# This function takes a role and a crime, and generates a clue based on the role's weights.
# The clue can be incriminating, misleading, social, or random.
# -----------------------------
def recall_player_memory(crime, guilty, innocent, lovers, weights):
    # Pick a memory type based on the role's weights
    mem_type = weighted_choice(weights)

    if mem_type == "incriminating":
        mem_options = [
            lambda: weapon_noise_memory(crime, 1),
            lambda: weapon_evidence_memory(crime, 1),
            lambda: room_memory(crime, 1),
            lambda: movement_memory(crime, guilty, innocent, 1)
        ]
        # Randomly select and execute one
        return random.choice(mem_options)()

    if mem_type == "misleading":
        mem_options = [
            lambda: weapon_noise_memory(crime, 0),
            lambda: weapon_evidence_memory(crime, 0),
            lambda: room_memory(crime, 0),
            lambda: movement_memory(crime, guilty, innocent, 0)
        ]
        # Randomly select and execute one
        return random.choice(mem_options)()

    if mem_type == "social":
        return social_memory(lovers, guilty, innocent)

    return random_memory()


