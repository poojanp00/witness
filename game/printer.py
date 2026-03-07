# -----------------------------
# PRINT FUNCTION
# -----------------------------
# This function prints the crime details and the clues provided by each witness.
# -------------------------------
import random
from game.data.roles import culprits, guests

def print_mystery(crime, clues):

    print("\nCRIME (hidden from players)")
    print("----------------------------")
    print(f"Culprit: {crime['culprit']}")
    print(f"Weapon: {crime['weapon']}")
    print(f"Room: {crime['room']}")
    print(f"Time: {crime['time']}")

    print("\nWITNESS CLUES")
    print("----------------------------")

    for person,clue_list in clues.items():

        roles = {**culprits, **guests}
        print(f"\n{person} ({roles[person]})")
        random.shuffle(clue_list)
        for i,c in enumerate(clue_list,1):
            print(f"{i}. {c}")