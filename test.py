import random
from datetime import datetime, timedelta

# -----------------------------
# CORE GAME DATA
# -----------------------------

killer = ["Alex"]
guests = ["Sam","Morgan","Riley","Jordan","Taylor","Casey","Avery"]
weapons = ["knife","rope","gun","poison"]

locations = [
  "courtyard",
  "balcony",
  "terrace",
  "kitchen",
  "sauna",
  "library",
  "ballroom",
  "dining room",
  "garden",
  "wine cellar"
]

roles = {
    "Alex":"culprit",
    "Sam":"accomplice",
    "Morgan":"detective",
    "Riley":"lover",
    "Jordan":"lover",
    "Taylor":"rival",
    "Casey":"gossip",
    "Avery":"clueless"
}

# -----------------------------
# CLUE TYPE WEIGHTS
# -----------------------------

role_weights = {
    "detective": {"crime":50,"social":15,"red":10,"random":10},
    "culprit": {"crime":10,"social":20,"red":40,"random":20},
    "accomplice": {"crime":20,"social":20,"red":30,"random":20},
    "lover": {"crime":35,"social":20,"red":10,"random":15},
    "rival": {"crime":20,"social":15,"red":45,"random":15},
    "gossip": {"crime":25,"social":35,"red":15,"random":15},
    "clueless": {"crime":25,"social":20,"red":15,"random":25}
}

# -----------------------------
# FRAGMENT POOLS
# -----------------------------

observer_phrases = [
    "I saw",
    "I noticed",
    "I think I saw",
    "I could have sworn I saw",
    "I briefly noticed",
    "I remember seeing",
    "I might be mistaken but I saw",
    "I clearly remember",
    "I caught a glimpse of",
    "I might have seen",
    "I heard"
]

subjects = [
    "someone",
    "a figure",
    "a silhouette",
    "a blur",
    "two people",
]

crime_events = [
    "leaving",
    "entering",
    "standing near",
    "walking towards",
    "rushing away from",
    "lingering around",
    "hurrying to",
    "wandering by",
    "pacing around",
    "hiding near",
    "seeming nervous around",
]

time_phrases = [
    "around {crime_time}",
    "just before {crime_time}",
    "just after {crime_time}",
    "moments before {crime_time}",
    "moments after {crime_time}",
    "shortly before {crime_time}",
    "shortly after {crime_time}",
    "not long before {crime_time}",
    "not long after {crime_time}",
    "earlier in the evening",
    "later in the evening",
    "after everything happened",
    "sometime in the night",
    "before things got chaotic",
    "when most people were distracted"
]

social_events = [
    "arguing with someone near",
    "whispering in the vicinity of",
    "speaking in a hushed voice around",
    "having a tense conversation by",
    "seeming upset with each other in",
    "talking quietly close to the",
    "raising their voice by",
    "having a heated discussion by",
]


random_templates = [
    "dropped my drink",
    "was looking for food",
    "heard music",
    "noticed the lights flicker",
    "heard laughter from another room",
    "saw a cat lurking around",
    "was supposed to meet someone privately",
    "stepped outside for some air",
    "left quickly because I thought someone saw me",
]

# -----------------------------
# TIME GENERATION
# -----------------------------

def random_time():
    base = datetime.strptime("21:50","%H:%M")
    offset = random.randint(0,10)
    t = base + timedelta(minutes=offset)
    return t.strftime("%H:%M")

# -----------------------------
# CRIME GENERATION
# -----------------------------

def generate_crime():
    culprit = "Alex"  # fixed since Alex role
    weapon = random.choice(weapons)
    location = random.choice(locations)
    time = random_time()

    return {
        "culprit":culprit,
        "weapon":weapon,
        "location":location,
        "time":time
    }

# -----------------------------
# CLUE TYPE PICKER
# -----------------------------

def weighted_choice(weight_dict):
    total = sum(weight_dict.values())
    r = random.uniform(0,total)
    upto = 0
    for k,v in weight_dict.items():
        if upto+v >= r:
            return k
        upto += v

# -----------------------------
# CLUE GENERATORS
# -----------------------------

def observation_clue(crime, flag):
    obs = random.choice(observer_phrases)
    subj = random.choice(subjects + [crime["culprit"]])
    event = random.choice(crime_events)
    if flag == 1:
        loc = crime["location"]
        time_phrase = random.choice(time_phrases).format(crime_time=crime["time"])
        return f"{obs} {subj} {event} the {loc} {time_phrase}."
    else:
        wrong_loc = random.choice([loc for loc in locations if loc != crime["location"]])
        time = random.choice(time_phrases).format(crime_time=random_time())

        return f"{obs} {subj} {event} the {wrong_loc} {time}."

def social_clue():
    obs = random.choice(observer_phrases)
    subj = random.choice(subjects + guests + killer)
    event = random.choice(social_events)

    loc = random.choice(locations)
    time = random.choice(time_phrases).format(crime_time=random_time())

    return f"{obs} {subj} {event} the {loc} {time}."

def random_clue():
    random_event = random.choice(random_templates)
    time = random.choice(time_phrases).format(crime_time=random_time())

    return f"I {random_event} {time}."



noise_matrix = {
    "knife": [
        "a scream", "a scrape", "a clang", "a thud",
        "someone struggling", "a gasp", "something falling",
        "a muffled cry", "silence"
    ],

    "rope": [
        "a choking sound", "someone struggling", "a snap", "a thud",
        "someone gasping", "silence", "a muffled cry",
        "a scrape", "something falling"
    ],

    "gun": [
        "a scream", "a bang", "a gunshot", "a thud",
        "something falling", "a gasp", "silence",
        "a loud crack", "a muffled cry"
    ],

    "poison": [
        "a thud", "silence", "someone gasping", "a choking sound",
        "a muffled cry", "something falling", "a cough",
        "a scrape", "a groan"
    ]
}



# weapon_mat = {
#     "knife": ["a bloody knife", "a knife with fingerprints"],
#     "rope": ["a frayed rope", "a rope with fibers"],
#     "gun": ["a smoking gun", "a gun with a serial number"],
#     "poison": ["a vial of poison", "a poisoned drink"]
# }


# def weapon_clue(crime):
#     weapon_desc = random.choice(weapon_mat[crime["weapon"]])
#     loc = crime["location"]
#     time_phrase = random.choice(time_phrases).format(crime_time=crime["time"])

#     return f"I saw {weapon_desc} near the {loc} {time_phrase}."

def noise_clue(crime, flag):
    noise = random.choice(noise_matrix[crime["weapon"]])
    fake_noise_list = [n for w, n in noise_matrix.items() if w != crime["weapon"]]
    fake_noise = random.choice(random.choice(fake_noise_list))

    loc = crime["location"]
    time_phrase = random.choice(time_phrases).format(crime_time=crime["time"])
    wrong_loc = random.choice([loc for loc in locations if loc != crime["location"]])
    wrong_time = random.choice(time_phrases).format(crime_time=random_time())

    if flag == 1:
        # crime noise clue
        return f"I heard {noise} near the {loc} {time_phrase}."
    else:
        # red herring noise clue
        return f"I heard {fake_noise} near the {wrong_loc} {wrong_time}."
    

weapon_sight_matrix = {

    "knife": [
        "a flash of metal",
        "someone wiping something off a blade",
        "something shiny in someone's hand",
        "a blade catching the light",
        "someone quickly hiding a knife"
    ],

    "rope": [
        "a coil of rope",
        "someone holding a length of rope",
        "rope fibers on the ground",
        "something dangling from someone's hand",
        "a rope quickly stuffed into a pocket"
    ],

    "gun": [
        "a small handgun",
        "someone holding something metallic",
        "a flash from a muzzle",
        "someone tucking a gun away",
        "a dark object shaped like a pistol"
    ],

    "poison": [
        "a small vial",
        "someone pouring something into a drink",
        "a strange bottle on the table",
        "someone slipping something into a glass",
        "a small container quickly hidden"
    ]
}

def sight_clue(crime, flag):

    sight = random.choice(weapon_sight_matrix[crime["weapon"]])
    fake_list = [v for k,v in weapon_sight_matrix.items() if k != crime["weapon"]]
    fake_sight = random.choice(random.choice(fake_list))

    loc = crime["location"]
    time = random.choice(time_phrases).format(crime_time=crime["time"])

    wrong_loc = random.choice([l for l in locations if l != crime["location"]])
    wrong_time = random.choice(time_phrases).format(crime_time=random_time())

    if flag == 1:
        return f"I saw {sight} near the {loc} {time}."
    else:
        return f"I saw {fake_sight} near the {wrong_loc} {wrong_time}."

room_evidence = {
    "courtyard": [
        "wet stone footsteps",
        "a dropped garden glove",
        "mud tracked across the ground"
    ],

    "balcony": [
        "a chair knocked over",
        "a dropped glass",
        "scratches on the railing"
    ],

    "terrace": [
        "a broken wine glass",
        "a spilled drink",
        "chairs pushed aside"
    ],

    "kitchen": [
        "a knife missing from the rack",
        "water running in the sink",
        "a cutting board left out"
    ],

    "sauna": [
        "steam filling the air",
        "a towel left on the floor",
        "condensation on the door"
    ],

    "library": [
        "a book lying open",
        "a chair pulled out",
        "papers scattered on the desk"
    ],

    "ballroom": [
        "music still playing",
        "a dropped glove",
        "scuff marks on the floor"
    ],

    "dining room": [
        "a half-finished drink",
        "a chair knocked over",
        "a plate left untouched"
    ],

    "garden": [
        "fresh soil disturbed",
        "footprints in the dirt",
        "a broken branch"
    ],

    "wine cellar": [
        "a cracked bottle",
        "wine dripping on the floor",
        "a cork left nearby"
    ]
}

def room_clue(crime, flag):

    if flag == 1:
        evidence = random.choice(room_evidence[crime["location"]])
        loc = crime["location"]
        time = random.choice(time_phrases).format(crime_time=crime["time"])
        return f"I noticed {evidence} in the {loc} {time}."

    else:
        wrong_loc = random.choice([l for l in locations if l != crime["location"]])
        evidence = random.choice(room_evidence[wrong_loc])
        time = random.choice(time_phrases).format(crime_time=random_time())
        return f"I noticed {evidence} in the {wrong_loc} {time}."
# -----------------------------
# CLUE FACTORY
# -----------------------------

def generate_clue(role, crime):

    clue_type = weighted_choice(role_weights[role])

    if clue_type == "crime":
        if random.random() < 0.25:
            return noise_clue(crime, 1) # crime noise clue
        if 0.25 < random.random() < 0.50:
            return sight_clue(crime, 1) # crime weapon sight clue
        if 0.50 < random.random() < 0.75:
            return room_clue(crime, 1) # crime room clue
        return observation_clue(crime, 1)

    if clue_type == "red":
        if random.random() < 0.25:
            return noise_clue(crime, 0) # red herring noise clue
        if 0.25 < random.random() < 0.50:
            return sight_clue(crime, 0) # red herring weapon sight clue
        if 0.50 < random.random() < 0.75:
            return room_clue(crime, 0) # red herring room clue
        return observation_clue(crime, 0)

    if clue_type == "social":
        return social_clue()

    return random_clue()

# -----------------------------
# MAIN GENERATOR
# -----------------------------

def generate_mystery():

    crime = generate_crime()

    clues = {}

    all_guests = guests + killer

    for person in all_guests:

        role = roles[person]

        clues[person] = []

        for i in range(5):
            clue = generate_clue(role, crime)
            clues[person].append(clue)

    return crime, clues

# -----------------------------
# PRINT OUTPUT
# -----------------------------

def print_mystery(crime, clues):

    print("\nCRIME (hidden from players)")
    print("----------------------------")
    print(f"Culprit: {crime['culprit']}")
    print(f"Weapon: {crime['weapon']}")
    print(f"Location: {crime['location']}")
    print(f"Time: {crime['time']}")

    print("\nWITNESS CLUES")
    print("----------------------------")

    for person,clue_list in clues.items():

        print(f"\n{person} ({roles[person]})")
        random.shuffle(clue_list)
        for i,c in enumerate(clue_list,1):
            print(f"{i}. {c}")


def test():
    #test 25 clues of each type
    crime = generate_crime()
    print("CRIME:", crime)
    for i in range(5):
        print("CRIME CLUE:", observation_clue(crime, 1))
        print("CRIME NOISE CLUE:", noise_clue(crime, 1))
        print("CRIME WEAPON CLUE:", sight_clue(crime, 1))
        print("CRIME ROOM CLUE:", room_clue(crime, 1))
        print("\n\n")
        print("RH CLUE:", observation_clue(crime, 0))
        print("RH NOISE CLUE:", noise_clue(crime, 0))
        print("RH SIGHT CLUE:", sight_clue(crime, 0))
        print("RH ROOM CLUE:", room_clue(crime, 0))
        print("\n\n")
        print("SOCIAL CLUE:", social_clue())
        print("RANDOM CLUE:", random_clue())

        print("\n\n\n\n\n\n\n\n")


# -----------------------------
# RUN
# -----------------------------

crime, clues = generate_mystery()
print_mystery(crime, clues)
# test() 