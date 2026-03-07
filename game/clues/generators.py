# -------------------------------
# CLUE GENERATION
# -------------------------------
# Generate different types of clues based on crime and flag.
# Flag determines if clue should be incriminating or misleading. 
# -------------------------------
import random
from game.data.fragments import observations, subjects, movements, social, randoms, times
from game.data.artifacts import weapons, rooms 

from game.utils.time_utils import random_time

# -------------------------------
# MOVEMENT CLUE GENERATION
# -------------------------------
def movement_clue(crime, guilty, innocent, flag):
    observation = random.choice(observations)
    movement = random.choice(movements)

    if flag == 1: # INCRIMIINATING CLUE
        room = crime["room"]
        subject = random.choice(subjects + guilty)
        time_phrase = random.choice(times).format(crime_time=crime["time"])

        clue = f"INC: I {observation} {subject} {movement} the {room} {time_phrase}."
        return clue

    else: # MISLEADING
        wrong_room = random.choice([r for r in rooms.keys() if r != crime["room"]])
        wrong_time = random.choice(times).format(crime_time=random_time())
        wrong_subject = random.choice(subjects + innocent)
        
        clue = f"MISL: I {observation} {wrong_subject} {movement} the {wrong_room} {wrong_time}."
        return clue

# -------------------------------
# NOISE CLUE GENERATION
# -------------------------------
def noise_clue(crime, flag):
    if flag == 1: # INCRIMIINATING CLUE
        noise = random.choice(weapons[crime["weapon"]]["noises"])
        room = crime["room"]
        time = random.choice(times).format(crime_time=crime["time"])
        clue = f"INC: I heard {noise} near the {room} {time}."
        return clue

    else: # MISLEADING CLUE
        other_weapons = [w for w in weapons.keys() if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        wrong_noise = random.choice(weapons[wrong_weapon]["noises"])
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_time = random.choice(times).format(crime_time=random_time())
        clue = f"MISL: I heard {wrong_noise} near the {wrong_room} {wrong_time}."
        return clue

# -------------------------------
# WEAPON CLUE GENERATION
# -------------------------------
def weapon_clue(crime, flag):
    if flag == 1: # INCRIMINATING CLUE
        sight = random.choice(weapons[crime["weapon"]]["sights"])
        room = crime["room"]
        time = random.choice(times).format(crime_time=crime["time"])
        clue = f"INC: I saw {sight} near the {room} {time}."
        return clue

    else: # MISLEADING CLUE
        other_weapons = [w for w in weapons if w != crime["weapon"]]
        wrong_weapon = random.choice(other_weapons)
        wrong_sight = random.choice(weapons[wrong_weapon]["sights"])
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_time = random.choice(times).format(crime_time=random_time())
        clue = f"MISL: I saw {wrong_sight} near the {wrong_room} {wrong_time}."
        return clue
    

# -------------------------------
# ROOM CLUE GENERATION
# -------------------------------
def room_clue(crime, flag):
    if flag == 1: # INCRIMINATING CLUE
        evidence = random.choice(rooms[crime["room"]])
        room = crime["room"]
        time = random.choice(times).format(crime_time=crime["time"])
        clue = f"INC: I noticed {evidence} in the {room} {time}."
        return clue

    else: # MISLEADING CLUE
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_evidence = random.choice(rooms[wrong_room])
        wrong_time = random.choice(times).format(crime_time=random_time())
        clue = f"MISL: I noticed {wrong_evidence} in the {wrong_room} {wrong_time}."
        return clue
    
# -------------------------------
# SOCIAL CLUE GENERATION
# -------------------------------
def social_clue(guilty, innocent):
    observation = random.choice(observations)
    all_players = subjects + guilty + innocent
    subject = random.choice(all_players)
    social_event = random.choice(social)

    room = random.choice(list(rooms.keys()))
    time = random.choice(times).format(crime_time=random_time())

    clue = f"I {observation} {subject} {social_event} the {room} {time}."
    return clue

# -------------------------------
# RANDOM CLUE GENERATION
# -------------------------------
def random_clue():
    random_event = random.choice(randoms)
    time = random.choice(times).format(crime_time=random_time())

    clue = f"I {random_event} {time}."
    return clue
