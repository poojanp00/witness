from game.crime import generate_crime
from game.clues.movement import movement_clue
from game.clues.noise import noise_clue
from game.clues.weapon import weapon_clue
from game.clues.room import room_clue
from game.clues.random import random_clue, social_clue

# -----------------------------
# Test
# -----------------------------


def test():
    #test 25 clues of each type
    crime = generate_crime()
    print("CRIME:", crime)
    for i in range(5):
        print("INCRIMINATING CLUES:")
        print("MOVEMENT:", movement_clue(crime, 1))
        print("NOISE:", noise_clue(crime, 1))
        print("WEAPON:", weapon_clue(crime, 1))
        print("ROOM:", room_clue(crime, 1))
        print("\n\n")
        print("MISLEADING CLUES:")
        print("MOVEMENT:", movement_clue(crime, 0))
        print("NOISE:", noise_clue(crime, 0))
        print("WEAPON:", weapon_clue(crime, 0))
        print("ROOM:", room_clue(crime, 0))
        print("\n\n")
        print("SOCIAL CLUE:", social_clue())
        print("RANDOM CLUE:", random_clue())

        print("\n\n\n\n\n\n\n\n")
    return True


# -----------------------------
# RUN
# -----------------------------

# crime, clues = generate_mystery()
# print_mystery(crime, clues)
test() 