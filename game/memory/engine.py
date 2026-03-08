# -----------------------------
# GAME ENGINE
# -----------------------------

import random

from game.memory.generators import room_noise_memory, room_evidence_memory, movement_memory, weapon_noise_memory, weapon_evidence_memory, random_memory, incrim_social_memory, lover_social_memory, mislead_social_memory

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
# This function takes a crime and generates a clue based on the role's weights.
# Crime dict contains: weapon, room, time, guilty, innocent, lovers
# The clue can be incriminating, misleading, social, or random.
# -----------------------------
def recall_player_memory(crime, weights, role):
    # Pick a memory type based on the role's weights
    mem_type = weighted_choice(weights)

    if mem_type == "incriminating":
        mem_options = [
            # Category 1: WEAPON (25% chance) -> Then 50/50 Noise or Evidence
            lambda: random.choice([weapon_noise_memory, weapon_evidence_memory])(crime, role, 1),
            # Category 2: ROOM (25% chance) -> Then 50/50 Noise or Evidence
            lambda: random.choice([room_noise_memory, room_evidence_memory])(crime, role, 1),
            # Category 3: MOVEMENT (25% chance)
            lambda: movement_memory(crime, role, 1),
            # Category 4: SOCIAL (25% chance)
            lambda: incrim_social_memory(crime, role)
        ]
        # Randomly select and execute one category, then execute internal choice if needed
        return random.choice(mem_options)()

    if mem_type == "misleading":
        mem_options = [
            # Category 1: WEAPON (33% chance) -> Then 50/50 Noise or Evidence
            lambda: random.choice([weapon_noise_memory, weapon_evidence_memory])(crime, role, 0),
            # Category 2: ROOM (33% chance) -> Then 50/50 Noise or Evidence
            lambda: random.choice([room_noise_memory, room_evidence_memory])(crime, role, 0),
            # Category 3: MOVEMENT (33% chance)
            lambda: movement_memory(crime, role, 0),
            # Category 4: SOCIAL (25% chance)
            lambda: mislead_social_memory(crime, role)
        ]
        # Randomly select and execute one category, then execute internal choice if needed
        return random.choice(mem_options)()

    if mem_type == "social":
        mem_options = [
            # Category 1: Guilty (40% chance)
            lambda: incrim_social_memory(crime, role),
            lambda: incrim_social_memory(crime, role),
            # Category 2: Lovers (40% chance)
            lambda: lover_social_memory(crime, role),
            lambda: lover_social_memory(crime, role),
            # Category 3: Innocent (20% chance)
            lambda: mislead_social_memory(crime, role)
        ]
        return random.choice(mem_options)()

    return random_memory(role)


