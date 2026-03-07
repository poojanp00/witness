import random

from game.data.weapon import weapons
from game.data.room import rooms
from game.utils.time_utils import random_time

# -----------------------------
# CRIME GENERATION
# -----------------------------
# This function generates a crime with a fixed culprit
# and a random weapon, room, and time.
# -----------------------------
def generate_crime():
    culprit = "Alex"  # fixed for now
    weapon = random.choice(weapons)
    room = random.choice(rooms)
    time = random_time()

    return {
        "culprit":culprit,
        "weapon":weapon,
        "room":room,
        "time":time
    }