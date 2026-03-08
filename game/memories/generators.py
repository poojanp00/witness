# -------------------------------
# MEMORY GENERATION
# -------------------------------
# Generate different types of clues based on crime and flag.
# Flag determines if clue should be incriminating or misleading. 
# -------------------------------
import random
from game.data.fragments import OBSERVATIONS, SUBJECTS, AREAS, MOVEMENTS, GUILTY_SOCIAL, LOVER_SOCIAL, SOCIAL, SOLO_SOCIAL, RANDOMS, TIMES1, TIMES2, TIMES3
from game.data.artifacts import WEAPONS, ROOMS 

from game.utils.time_utils import random_time

# -------------------------------
# MOVEMENT MEMORY GENERATION
# -------------------------------
def movement_memory(crime, guilty, innocent, flag, role):
    observation = random.choice(OBSERVATIONS)
    movement = random.choice(MOVEMENTS)

    if flag == 1: # INCRIMIINATING MEMORY
        room = crime["room"]
        subject = random.choice(SUBJECTS+guilty)
        time_phrase = random.choice(TIMES1).format(crime_time=crime["time"])
        area = random.choice(AREAS)
        mems = [
            f"I {observation} {subject} {movement} the {room}.",
            f"I {observation} {subject} {movement} {area} {time_phrase}."
        ]
        return (random.choice(mems), "INC_MOV")

    else: # MISLEADING
        wrong_room = random.choice([r for r in ROOMS.keys() if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        wrong_subject = random.choice(SUBJECTS + innocent)
        area = random.choice(AREAS)
        mems = [
            f"I {observation} {wrong_subject} {movement} the {wrong_room}.",
            f"I {observation} {wrong_subject} {movement} {area} {wrong_time}."
        ]
        return (random.choice(mems), "MISL_MOV")

# -------------------------------
# WEAPON NOISE MEMORY GENERATION
# -------------------------------
def weapon_noise_memory(crime, flag, role):
    if flag == 1: # INCRIMIINATING MEMORY
        noise = random.choice(WEAPONS[crime["weapon"]]["noises"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I heard {noise} near the {room}.",
            f"I heard {noise} {time}."
        ]
        return (random.choice(mem), "INC_WPN_NSE")

    else: # MISLEADING MEMORY
        other_weapons = [w for w in WEAPONS.keys() if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        wrong_noise = random.choice(WEAPONS[wrong_weapon]["noises"])
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I heard {wrong_noise} near the {wrong_room}.",
            f"I heard {wrong_noise} {wrong_time}."
        ]
        return (random.choice(mem), "MISL_WPN_NSE")

# -------------------------------
# WEAPON EVIDENCE MEMORY GENERATION
# -------------------------------
def weapon_evidence_memory(crime, flag, role):
    if flag == 1: # INCRIMINATING MEMORY
        evidence = random.choice(WEAPONS[crime["weapon"]]["evidence"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I saw {evidence} near the {room}.",
            f"I saw {evidence} {time}.",
        ]
        return (random.choice(mem), "INC_WPN_EVI")

    else: # MISLEADING MEMORY
        other_weapons = [w for w in WEAPONS if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        evidence = random.choice(WEAPONS[wrong_weapon]["evidence"])
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I saw {evidence} near the {wrong_room}.",
            f"I saw {evidence} {wrong_time}."
        ]
        return (random.choice(mem), "MISL_WPN_EVI")
    

# -------------------------------
# ROOM NOISE MEMORY GENERATION
# -------------------------------
def room_noise_memory(crime, flag, role):
    if flag == 1: # INCRIMINATING MEMORY
        noise = random.choice(ROOMS[crime["room"]]["noises"])
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I heard {noise}.",
            f"I heard {noise} {time}."
        ]
        return (random.choice(mem), "INC_RM_NSE")

    else: # MISLEADING MEMORY
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_noise = random.choice(ROOMS[wrong_room]["noises"])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I heard {wrong_noise}.",
            f"I heard {wrong_noise} {wrong_time}."
        ]
        return (random.choice(mem), "MISL_RM_NSE")

# -------------------------------
# ROOM EVIDENCE MEMORY GENERATION
# -------------------------------
def room_evidence_memory(crime, flag, role):
    if flag == 1: # INCRIMINATING MEMORY
        evidence = random.choice(ROOMS[crime["room"]]["evidence"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I noticed {evidence} by the {room}.",
            f"I noticed {evidence} {time}."
        ]
        return (random.choice(mem), "INC_RM_EVI")

    else: # MISLEADING MEMORY
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_evidence = random.choice(ROOMS[wrong_room]["evidence"])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I noticed {wrong_evidence} by the {wrong_room}.",
            f"I noticed {wrong_evidence} {wrong_time}."
        ]
        return (random.choice(mem), "MISL_RM_EVI")
    
# -------------------------------
# SOCIAL MEMORY GENERATION
# -------------------------------
def incrim_social_memory(guilty, role):
    guilty_copy = guilty.copy()
    random.shuffle(guilty_copy)
    social = random.choice(GUILTY_SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    return (f"{guilty_copy[0]} {social} {guilty_copy[1]} {time}.", "INC_SOC")

def lover_social_memory(lovers, role):
    lovers_copy = lovers.copy()
    random.shuffle(lovers_copy)
    social = random.choice(LOVER_SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    return (f"{lovers_copy[0]} {social} {lovers_copy[1]} {time}.", "LOV_SOC")

def mislead_social_memory(person_a, person_b, role):
    social = random.choice(SOCIAL)
    solo_social = random.choice(SOLO_SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    mem = [
        f"{person_a} {social} {person_b} {time}.",
        f"{person_a} {solo_social}.",
        f"{person_b} {solo_social}."
    ]
    return (random.choice(mem), "MISL_SOC")
    
# -------------------------------
# RANDOM MEMORY GENERATION
# -------------------------------
def random_memory(role):
    i_random = random.choice(RANDOMS)
    time = random.choice(TIMES3).format(crime_time=random_time())

    mem = [
        f"I {i_random} {time}.",
        f"Someone {i_random} {time}.",
    ]
    return (random.choice(mem), "RAND")
