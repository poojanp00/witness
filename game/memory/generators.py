# -------------------------------
# MEMORY GENERATION
# -------------------------------
# Generate different types of clues based on crime and flag.
# Flag determines if clue should be incriminating or misleading. 
# -------------------------------
import random
from game.data.fragments import OBS_CLEAR, OBS_VAGUE, SUBJECTS, AREAS, MOVEMENTS, GUILTY_SOCIAL, LOVER_SOCIAL, SOCIAL, SOLO_SOCIAL, RANDOMS, TIMES1, TIMES2, TIMES3
from game.data.artifacts import WEAPONS, ROOMS 

from game.utils.time import random_time

# -------------------------------
# MOVEMENT MEMORY GENERATION
# -------------------------------
def movement_memory(crime, role, flag):
    guilty = crime["guilty"]
    innocent = crime["innocent"]
    movement = random.choice(MOVEMENTS)

    if role == "detective":
        obs = random.choice(OBS_CLEAR)
    elif role == "clueless":
        obs = random.choice(OBS_VAGUE)
    else:
        obs = random.choice(OBS_CLEAR+OBS_VAGUE)

    if flag == 1: # INCRIMIINATING MEMORY
        room = crime["room"]
        subject = random.choice(SUBJECTS+guilty)
        time_phrase = random.choice(TIMES1).format(crime_time=crime["time"])
        area = random.choice(AREAS)
        mems = [
            f"I {obs} {subject} {movement} the {room}.",
            f"I {obs} {subject} {movement} {area} {time_phrase}."
        ]
        return (random.choice(mems), "INC_MOV")

    else: # MISLEADING
        if role == "clueless":
            obs = random.choice(OBS_VAGUE)
        else:
            obs = random.choice(OBS_CLEAR+OBS_VAGUE)

        wrong_room = random.choice([r for r in ROOMS.keys() if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        wrong_subject = random.choice(SUBJECTS + innocent)
        area = random.choice(AREAS)
        mems = [
            f"I {obs} {wrong_subject} {movement} the {wrong_room}.",
            f"I {obs} {wrong_subject} {movement} {area} {wrong_time}."
        ]
        return (random.choice(mems), "MISL_MOV")

# -------------------------------
# WEAPON NOISE MEMORY GENERATION
# -------------------------------
def weapon_noise_memory(crime, role, flag):
    if flag == 1: # INCRIMIINATING MEMORY
        noise = random.choice(WEAPONS[crime["weapon"]]["noises"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I heard {noise} near the {room}.",
            f"I heard {noise} {time}.",
            f"I heard {noise}.",
        ]
        return (random.choice(mem), "INC_WPN_NSE")

    else: # MISLEADING MEMORY
        other_weapons = [w for w in WEAPONS.keys() if w != crime["weapon"]]
        weapon = random.choice(other_weapons)
        noise = random.choice(WEAPONS[weapon]["noises"])
        room = random.choice([r for r in ROOMS if r != crime["room"]])
        time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I heard {noise} near the {room}.",
            f"I heard {noise} {time}.",
            f"I heard {noise}."
        ]
        return (random.choice(mem), "MISL_WPN_NSE")

# -------------------------------
# WEAPON EVIDENCE MEMORY GENERATION
# -------------------------------
def weapon_evidence_memory(crime, role, flag):
    if flag == 1: # INCRIMINATING MEMORY
        if role == "detective":
            obs = random.choice(OBS_CLEAR)
        elif role == "clueless":
            obs = random.choice(OBS_VAGUE)
        else:
            obs = random.choice(OBS_CLEAR+OBS_VAGUE)

        evidence = random.choice(WEAPONS[crime["weapon"]]["evidence"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I {obs} {evidence} near the {room}.",
            f"I {obs} {evidence}.",
            f"I {obs} {evidence} {time}.",
        ]
        return (random.choice(mem), "INC_WPN_EVI")

    else: # MISLEADING MEMORY
        if role == "clueless":
            obs = random.choice(OBS_VAGUE)
        else:
            obs = random.choice(OBS_CLEAR+OBS_VAGUE)

        other_weapons = [w for w in WEAPONS if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        evidence = random.choice(WEAPONS[wrong_weapon]["evidence"])
        room = random.choice([r for r in ROOMS if r != crime["room"]])
        time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I {obs} {evidence} near the {room}.",
            f"I {obs} {evidence}."
            f"I {obs} {evidence} {time}."
        ]
        return (random.choice(mem), "MISL_WPN_EVI")
    

# -------------------------------
# ROOM NOISE MEMORY GENERATION
# -------------------------------
def room_noise_memory(crime, role, flag):
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
def room_evidence_memory(crime, role, flag):
    if flag == 1: # INCRIMINATING MEMORY
        if role == "detective":
            observation = random.choice(OBS_CLEAR)
        elif role == "clueless":
            observation = random.choice(OBS_VAGUE)
        else:
            observation = random.choice(OBS_CLEAR+OBS_VAGUE)

        evidence = random.choice(ROOMS[crime["room"]]["evidence"])
        area = random.choice(AREAS)
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I {observation} {evidence} around {area}.",
            f"I {observation} {evidence} {time}."

        ]
        return (random.choice(mem), "INC_RM_EVI")

    else: # MISLEADING MEMORY
        if role == "clueless":
            observation = random.choice(OBS_VAGUE)
        else:
            observation = random.choice(OBS_CLEAR+OBS_VAGUE)
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        area = random.choice(AREAS)
        wrong_evidence = random.choice(ROOMS[wrong_room]["evidence"])
        time = random.choice(TIMES2+TIMES3).format(crime_time=crime["time"])
        mem = [
            f"I {observation} {wrong_evidence} around {area}.",
            f"I {observation} {wrong_evidence} {time}."
        ]
        return (random.choice(mem), "MISL_RM_EVI")
    
# -------------------------------
# SOCIAL MEMORY GENERATION
# -------------------------------
def incrim_social_memory(crime, role):
    guilty = crime["guilty"]
    person1, person2 = random.sample(guilty, 2)
    social = random.choice(GUILTY_SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    return (f"{person1} {social} {person2} {time}.", "INC_SOC")

def lover_social_memory(crime, role):
    lovers = crime["lovers"]
    person1, person2 = random.sample(lovers, 2)
    social = random.choice(LOVER_SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    return (f"{person1} {social} {person2} {time}.", "LOV_SOC")

def mislead_social_memory(crime, role):
    innocents = crime["innocent"]
    person1, person2 = random.sample(innocents, 2)
    social = random.choice(SOCIAL)
    solo_social = random.choice(SOLO_SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    mem = [
        f"{person1} {social} {person2} {time}.",
        f"{person1} {solo_social}.",
        f"{person2} {solo_social}."
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
