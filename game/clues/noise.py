import random

from game.data.noise import noise_matrix
from game.data.room import rooms
from game.data.time import times
from game.utils.time_utils import random_time

# -------------------------------
# NOISE CLUE GENERATION
# -------------------------------
# This function generates a noise clue based on the crime and a flag.
# The flag determines if the clue should be incriminating or misleading.
# -------------------------------

def noise_clue(crime, flag):
    # INCRIMINATING CLUE
    if flag == 1:
        noise = random.choice(noise_matrix[crime["weapon"]])
        room = crime["room"]
        time = random.choice(times).format(crime_time=crime["time"])

        incriminating_clue = f"INC: I heard {noise} near the {room} {time}."
        return incriminating_clue

    # MISLEADING CLUE
    else:
        wrong_noise_list = [n for w, n in noise_matrix.items() if w != crime["weapon"]]
        wrong_noise = random.choice(random.choice(wrong_noise_list))
        wrong_room = random.choice([r for r in rooms if r != crime["room"]])
        wrong_time = random.choice(times).format(crime_time=random_time())

        misleading_clue = f"MISL: I heard {wrong_noise} near the {wrong_room} {wrong_time}."
        return misleading_clue