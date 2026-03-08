# -------------------------------
# MEMORY GENERATION
# -------------------------------
# Generate different types of clues based on crime and flag.
# Flag determines if clue should be incriminating or misleading. 
# -------------------------------
import random
from game.data.fragments import OBSERVATIONS, SUBJECTS, AREAS, MOVEMENTS, GUILTY_SOCIAL, LOVER_SOCIAL, SOCIAL, RANDOMS, TIMES1, TIMES2, TIMES3
from game.data.artifacts import WEAPONS, ROOMS 

from game.utils.time_utils import random_time

# -------------------------------
# MOVEMENT MEMORY GENERATION
# -------------------------------
def movement_memory(crime, guilty, innocent, flag):
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
        return random.choice(mems)

    else: # MISLEADING
        wrong_room = random.choice([r for r in ROOMS.keys() if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        wrong_subject = random.choice(SUBJECTS + innocent)
        area = random.choice(AREAS)
        mems = [
            f"I {observation} {wrong_subject} {movement} the {wrong_room}.",
            f"I {observation} {wrong_subject} {movement} {area} {wrong_time}."
        ]
        return random.choice(mems)

# -------------------------------
# WEAPON NOISE MEMORY GENERATION
# -------------------------------
def weapon_noise_memory(crime, flag):
    if flag == 1: # INCRIMIINATING MEMORY
        noise = random.choice(WEAPONS[crime["weapon"]]["noises"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"NOISE_INC: I heard {noise} near the {room}.",
            f"NOISE_INC: I heard {noise} {time}."
        ]
        return random.choice(mem)

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
        return random.choice(mem)

# -------------------------------
# WEAPON EVIDENCE MEMORY GENERATION
# -------------------------------
def weapon_evidence_memory(crime, flag):
    if flag == 1: # INCRIMINATING MEMORY
        evidence = random.choice(WEAPONS[crime["weapon"]]["evidence"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I saw {evidence} near the {room}.",
            f"I saw {evidence} {time}.",

        ]
        return random.choice(mem)

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
        return random.choice(mem)
    

# -------------------------------
# ROOM MEMORY GENERATION
# -------------------------------
def room_memory(crime, flag):
    if flag == 1: # INCRIMINATING MEMORY
        evidence = random.choice(ROOMS[crime["room"]]["evidence"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        mem = [
            f"I noticed {evidence} by the {room}.",
            f"I noticed {evidence} {time}."
        ]
        return random.choice(mem)

    else: # MISLEADING MEMORY
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_evidence = random.choice(ROOMS[wrong_room]["evidence"])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        mem = [
            f"I noticed {wrong_evidence} by the {wrong_room}.",
            f"I noticed {wrong_evidence} {wrong_time}."
        ]
        return random.choice(mem)
    
# -------------------------------
# SOCIAL MEMORY GENERATION
# -------------------------------
def social_memory(lovers, guilty, innocent):
    roll = random.random()
    lover_social = random.choice(LOVER_SOCIAL)
    guilty_social = random.choice(GUILTY_SOCIAL)
    random_social = random.choice(SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())
    if roll < 0.4 :
        random.shuffle(guilty)
        mem = f"{guilty[0]} {guilty_social} {guilty[1]} {time}."
        return mem
    if 0.4 < roll < 0.8:
        random.shuffle(lovers)
        mem = f"{lovers[0]} {lover_social} {lovers[1]} {time}."
        return mem 
    else:
        innocent_pair = random.sample(innocent, 2) # all guests
        mem = f"{innocent_pair[0]} {random_social} {innocent_pair[1]} {time}."
        return mem
    
    
    

    

# -------------------------------
# RANDOM MEMORY GENERATION
# -------------------------------
def random_memory():
    i_random = random.choice(RANDOMS)
    time = random.choice(TIMES3).format(crime_time=random_time())

    clue = [
        f"I {i_random} {time}.",
        f"Someone {i_random} {time}.",
    ]
    return random.choice(clue)
