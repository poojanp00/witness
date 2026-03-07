import random

from game.data.weapon import weapons_matrix
from game.data.room import rooms
from game.data.time import times
from game.utils.time_utils import random_time

# -------------------------------
# WEAPON CLUE GENERATION
# -------------------------------
# This function generates a weapon clue based on the crime and a flag.
# The flag determines if the clue should be incriminating or misleading.
# -------------------------------
def weapon_clue(crime, flag):
    # INCRIMINATING CLUE
    if flag == 1:
        sight = random.choice(weapons_matrix[crime["weapon"]])
        room = crime["room"]
        time = random.choice(times).format(crime_time=crime["time"])

        incriminating_clue = f"INC: I saw {sight} near the {room} {time}."
        return incriminating_clue

    # MISLEADING CLUE
    else:
        wrong_sights_list = [v for k,v in weapons_matrix.items() if k != crime["weapon"]]
        wrong_sight = random.choice(random.choice(wrong_sights_list))
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_time = random.choice(times).format(crime_time=random_time())

        misleading_clue = f"MISL: I saw {wrong_sight} near the {wrong_room} {wrong_time}."
        return misleading_clue