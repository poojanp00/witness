import random
import json
from game.data.artifacts import ROLES, WEAPONS, ROOMS
from game.clues.engine import recall_player_memory
from game.utils.time_utils import random_time

# -----------------------------
# CRIME GENERATION
# -----------------------------
# This function generates a crime with a fixed culprit
# and a random weapon, room, and time.
# -----------------------------
def generate_crime(assignments):
    culprit = [name for name, data in assignments.items() if data["role"] == "culprit"][0]
    accomplice = [name for name, data in assignments.items() if data["role"] == "accomplice"]
    weapon = random.choice(list(WEAPONS.keys()))
    room = random.choice(list(ROOMS.keys()))
    time = random_time()

    return {
        "culprit":culprit,
        "weapon":weapon,
        "room":room,
        "time":time
    }

def assign_roles(players):
    role_pool = ["detective", "culprit", "accomplice", "lover", "lover", "rival", "gossip", "accomplice", "clueless", "clueless"]
    # If you have fewer than 10 players, trim the pool
    role_pool = role_pool[:len(players)]
    
    random.shuffle(role_pool)
    random.shuffle(players)
    
    assignments = {}
    for i, name in enumerate(players):
        role = role_pool[i]
        assignments[name] = {
            "role": role,
            "dossier": ROLES[role], # Pulls the weights and schpeel
            "target": None,
            "partner": None
        }
    for name, data in assignments.items():
        # Assign a Target to the Rival
        if data["role"] == "rival":
            potential_targets = [p for p in players if p != name]
            data["target"] = random.choice(potential_targets)
            
        # Link the two Lovers so they know who to protect
        if data["role"] == "lover":
            partners = [p for p, d in assignments.items() if d["role"] == "lover" and p != name]
            if partners:
                data["partner"] = partners[0]

    return assignments


# -----------------------------
# MAIN GENERATOR
# -----------------------------
# This function generates a crime and clues for each witness based on their role.
# -----------------------------
def initialize_game(assignments):
    # 1. Generate the core crime data (Room, Weapon, Time)
    crime = generate_crime(assignments)
    guilty = [name for name, data in assignments.items() if data["role"] in ["culprit", "accomplice"]]
    innocent = [name for name, data in assignments.items() if name not in guilty]
    lovers = [name for name, data in assignments.items() if data["role"] == "lover"]

    # 2. Generate 5 personalized clues for each player
    clues = {
        name: [
            recall_player_memory(crime, guilty, innocent, lovers, data["dossier"]["weights"]) 
            for _ in range(7)
        ]
        for name, data in assignments.items()
    }
    return crime, clues

players = ["Poojan", "Diya", "Kishan", "Shalini", "Sonal", "Sandeep", "Baa"]
# crime, clues = 
# distribute_player_hands(players, crime, clues)
# print_mystery(crime, clues)
# print(clues)

assignments = assign_roles(players)
# print(assignments)
print("--- GAME ASSIGNMENTS ---")
for name, data in assignments.items():
    role_label = data["role"].upper()
    print(f"{name.ljust(12)} | Role: {role_label}")
print("\n\n")
player_clues = initialize_game(assignments)
# print(player_clues)
print(json.dumps(player_clues, indent=4))