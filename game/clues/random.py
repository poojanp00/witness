import random

from game.data.observation import observations
from game.data.subject import subjects
from game.data.event import social_events, random_events
from game.data.roles import guests, culprits
from game.data.room import rooms
from game.data.time import times
from game.utils.time_utils import random_time

# -------------------------------
# SOCIAL CLUE GENERATION
# -------------------------------
# This function generates a social clue based on the crime and a TODO: flag.
#  TODO: The flag determines if the clue should be incriminating or misleading.
# -------------------------------
def social_clue():
    observation = random.choice(observations)
    all_players = subjects + list(guests.keys()) + list(culprits.keys())
    subject = random.choice(all_players)
    social_event = random.choice(social_events)

    room = random.choice(rooms)
    time = random.choice(times).format(crime_time=random_time())

    clue = f"{observation} {subject} {social_event} the {room} {time}."
    return clue


# -------------------------------
# RANDOM CLUE GENERATION
# -------------------------------
# This function generates a random clue that is not necessarily related to the crime. 
# It can be used to add more depth and complexity to the game.
# -------------------------------
def random_clue():
    random_event = random.choice(random_events)
    time = random.choice(times).format(crime_time=random_time())

    clue = f"I {random_event} {time}."
    return clue
