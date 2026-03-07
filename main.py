import random

from game.data.roles import guests, culprits

from game.crime import generate_crime
from game.engine import generate_clue


from game.printer import print_mystery

# -----------------------------
# MAIN GENERATOR
# -----------------------------
# This function generates a crime and clues for each witness based on their role.
# -----------------------------
def generate_mystery():
    # 1. Generate the core crime data once
    crime = generate_crime()

    # 2. Merge roles into a single dictionary for O(1) lookup
    # This prevents rebuilding the dictionary inside the loop
    all_roles = {**guests, **culprits}
    
    # 3. Use dictionary comprehension for faster clue generation
    # Generating all 5 clues for each person in a single pass
    clues = {
        person: [generate_clue(role, crime) for _ in range(5)]
        for person, role in all_roles.items()
    }

    return crime, clues


# def distribute_player_hands(player_names, crime, clues):
#     # 1. Define the roles to be assigned
#     roles_pool = ["detective", "culprit", "accomplice", "lover", "lover", "rival", "gossip", "clueless"]
#     random.shuffle(roles_pool)
#     random.shuffle(player_names)

#     player_hands = {}

#     for i in range(len(player_names)):
#         name = player_names[i]
#         role = roles_pool[i]
        
#         # Get the clues generated for this specific role/person
#         # Assuming 'clues' is the dict from generate_mystery()
#         personal_clues = clues.get(name, ["No clues found for this witness."])

#         player_hands[name] = {
#             "role": role,
#             "dossier": get_dossier(role),
#             "clues": personal_clues
#         }
    
#     return player_hands

players = ["Poojan", "Diya", "Kishan", "Shalini", "Sonal", "Sandeep", "Baa"]
crime, clues = generate_mystery()
# distribute_player_hands(players, crime, clues)
print_mystery(crime, clues)
# print(clues)