import random

from game.data.room import rooms, rooms_matrix
from game.data.time import times
from game.utils.time_utils import random_time

# -------------------------------
# ROOM CLUE GENERATION
# -------------------------------
# This function generates a room clue based on the crime and a flag.
# The flag determines if the clue should be incriminating or misleading.
# -------------------------------
def room_clue(crime, flag):
    # INCRIMINATING CLUE
    if flag == 1:
        evidence = random.choice(rooms_matrix[crime["room"]])
        room = crime["room"]
        time = random.choice(times).format(crime_time=crime["time"])

        clue = f"INC: I noticed {evidence} in the {room} {time}."
        return clue

    # MISLEADING CLUE
    else:
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_evidence = random.choice(rooms_matrix[wrong_room])
        wrong_time = random.choice(times).format(crime_time=random_time())

        clue = f"MISL: I noticed {wrong_evidence} in the {wrong_room} {wrong_time}."
        return clue