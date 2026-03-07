import random

from game.data.observation import observations
from game.data.event import movements
from game.data.room import rooms
from game.data.subject import subjects
from game.data.roles import guests, culprits
from game.data.time import times
from game.utils.time_utils import random_time

# -------------------------------
# MOVEMENT CLUE GENERATION
# -------------------------------
# This function generates a clue based on the crime and a flag.
# The flag determines if the clue should be incriminating or misleading.
# -------------------------------
def movement_clue(crime, flag):
    observation = random.choice(observations)
    movement = random.choice(movements)

    # INCRIMIINATING CLUE
    if flag == 1:
        room = crime["room"]
        subject = random.choice(subjects + list(culprits.keys()))
        time_phrase = random.choice(times).format(crime_time=crime["time"])

        incriminating_clue = f"INC: {observation} {subject} {movement} the {room} {time_phrase}."
        return incriminating_clue

    # MISLEADING CLUE
    else:
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_time = random.choice(times).format(crime_time=random_time())
        wrong_subject = random.choice(subjects + list(guests.keys()))
        
        misleading_clue = f"MISL: {observation} {wrong_subject} {movement} the {wrong_room} {wrong_time}."
        return misleading_clue