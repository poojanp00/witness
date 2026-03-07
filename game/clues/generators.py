# -------------------------------
# CLUE GENERATION
# -------------------------------
# Generate different types of clues based on crime and flag.
# Flag determines if clue should be incriminating or misleading. 
# -------------------------------
import random
from game.data.fragments import OBSERVATIONS, SUBJECTS, AREAS, MOVEMENTS, SOCIAL, RANDOMS, TIMES1, TIMES2, TIMES3
from game.data.artifacts import WEAPONS, ROOMS 

from game.utils.time_utils import random_time

# -------------------------------
# MOVEMENT CLUE GENERATION
# -------------------------------
def movement_clue(crime, guilty, innocent, flag):
    observation = random.choice(OBSERVATIONS)
    movement = random.choice(MOVEMENTS)

    if flag == 1: # INCRIMIINATING CLUE
        room = crime["room"]
        subject = random.choice(SUBJECTS+guilty)
        time_phrase = random.choice(TIMES1).format(crime_time=crime["time"])
        area = random.choice(AREAS)
        clues = [
            f"MOVE_INC: I {observation} {subject} {movement} the {room}.",
            f"MOVE_INC: I {observation} {subject} {movement} {area} {time_phrase}."
        ]
        return random.choice(clues)

    else: # MISLEADING
        wrong_room = random.choice([r for r in ROOMS.keys() if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        wrong_subject = random.choice(SUBJECTS + innocent)
        area = random.choice(AREAS)
        clues = [
            f"MOVE_MISL: I {observation} {wrong_subject} {movement} the {wrong_room}.",
            f"MOVE_MISL: I {observation} {wrong_subject} {movement} {area} {wrong_time}."
        ]
        return random.choice(clues)

# -------------------------------
# NOISE CLUE GENERATION
# -------------------------------
def noise_clue(crime, flag):
    if flag == 1: # INCRIMIINATING CLUE
        noise = random.choice(WEAPONS[crime["weapon"]]["noises"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        clue = [
            f"NOISE_INC: I heard {noise} near the {room}.",
            f"NOISE_INC: I heard {noise} {time}."
        ]
        return random.choice(clue)

    else: # MISLEADING CLUE
        other_weapons = [w for w in WEAPONS.keys() if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        wrong_noise = random.choice(WEAPONS[wrong_weapon]["noises"])
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        clue = [
            f"NOISE_MISL: I heard {wrong_noise} near the {wrong_room}.",
            f"NOISE_MISL: I heard {wrong_noise} {wrong_time}."
        ]
        return random.choice(clue)

# -------------------------------
# WEAPON CLUE GENERATION
# -------------------------------
def weapon_clue(crime, flag):
    if flag == 1: # INCRIMINATING CLUE
        sight = random.choice(WEAPONS[crime["weapon"]]["sights"])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        clue = [
            f"WEAP_INC: I saw {sight} near the {room} {time}.",
            f"WEAP_INC: I saw {sight} {time}.",

        ]
        return random.choice(clue)

    else: # MISLEADING CLUE
        other_weapons = [w for w in WEAPONS if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        wrong_sight = random.choice(WEAPONS[wrong_weapon]["sights"])
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        clue = [
            f"WEAP_MISL: I saw {wrong_sight} near the {wrong_room}.",
            f"WEAP_MISL: I saw {wrong_sight} {wrong_time}."
        ]
        return random.choice(clue)
    

# -------------------------------
# ROOM CLUE GENERATION
# -------------------------------
def room_clue(crime, flag):
    if flag == 1: # INCRIMINATING CLUE
        evidence = random.choice(ROOMS[crime["room"]])
        room = crime["room"]
        time = random.choice(TIMES1).format(crime_time=crime["time"])
        clue = [
            f"ROOM_INC: I noticed {evidence} in the {room}.",
            f"ROOM_INC: I noticed {evidence} {time}."
        ]
        return random.choice(clue)

    else: # MISLEADING CLUE
        wrong_room = random.choice([r for r in ROOMS if r != crime["room"]])
        wrong_evidence = random.choice(ROOMS[wrong_room])
        wrong_time = random.choice(TIMES2+TIMES3).format(crime_time=random_time())
        clue = [
            f"ROOM_MISL: I noticed {wrong_evidence} in the {wrong_room}.",
            f"ROOM_MISL: I noticed {wrong_evidence} {wrong_time}."
        ]
        return random.choice(clue)
    
# -------------------------------
# SOCIAL CLUE GENERATION
# -------------------------------
def social_clue(pair):
    random.shuffle(pair)
    SOCIAL_event = random.choice(SOCIAL)
    time = random.choice(TIMES3).format(crime_time=random_time())

    clue = f"SOC: {pair[0]} {SOCIAL_event} {pair[1]} {time}."
    return clue

# -------------------------------
# RANDOM CLUE GENERATION
# -------------------------------
def random_clue():
    random_event = random.choice(RANDOMS)
    time = random.choice(TIMES3).format(crime_time=random_time())

    clue = f"RAND: I {random_event} {time}."
    return clue
