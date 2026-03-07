# -------------------------------
# ARTIFACTS
# -------------------------------
# File contains the artifacts and their details
# -------------------------------

ROLES = {
    "culprit": {
        "welcome": "The deed is done, and the adrenaline is fading. Now, the real work begins. You must blend in, fade into the background, and lead this pack of hounds on a wild goose chase.",
        "strategy": "You are the architect of confusion. Most of your memories are calculated fabrications designed to frame others. You rarely trip over your own story.",
        "objective": "Survive the votes. Deflect suspicion toward the Rivals or the innocent guests.",
        "weights": {
            "incriminating": 0,
            "social": 25,
            "misleading": 55,
            "random": 15
        }
    },
    "accomplice": {
        "welcome": "You saw what happened, and you've made your choice. You aren't the one with blood on your hands, but you’re the one holding the towel. If they go down, you go down.",
        "strategy": "You are a distraction expert. You remember many things that didn't actually happen, specifically to protect the Culprit. However, guilt is a heavy burden, and a true slip-up might occur.",
        "objective": "Keep the heat off the Culprit by flooding the conversation with red herrings.",
        "weights": {
            "incriminating": 10,
            "social": 35,
            "misleading": 50,
            "random": 5
        }
    },
    "detective": {
        "welcome": "The room is full of noise, but you only hear the discord. Your mind is a steel trap, and your eyes never miss a detail that others overlook.",
        "strategy": "You are the most reliable person in this room. Your clues are highly accurate and often pinpoint the specific location, weapon, or movements of the culprit.",
        "objective": "Filter out the gossip and lead the group toward the truth—but be careful, the culprit knows you are the biggest threat.",
        "weights": {
            "incriminating": 50,
            "social": 20,
            "misleading": 20,
            "random": 10
        }
    },
    "lover": {
        "welcome": "In a house full of strangers, you only have eyes for one person. Your heart is leading your head tonight, and you are fiercely protective of your inner circle.",
        "strategy": "You are observant but biased. You pay close attention to the people you care about, which gives you good insight, but you might unintentionally ignore the truth if it hurts someone you love.",
        "objective": "Share what you know, but decide for yourself who is worth protecting.",
        "weights": {
            "incriminating": 30,
            "social": 40,
            "misleading": 15,
            "random": 15
        }
    },
    "rival": {
        "welcome": "You didn't come here to make friends. Everyone has a secret, and you’re more than happy to expose them—especially if it makes your enemies look guilty.",
        "strategy": "You are cunning and chaotic. You remember a mix of truth and lies, often leaning toward 'misremembering' things that make your rivals look suspicious.",
        "objective": "Use the chaos to settle old scores, even if it means the real killer walks free.",
        "weights": {
            "incriminating": 25,
            "social": 15,
            "misleading": 45,
            "random": 15
        }
    },
    "gossip": {
        "welcome": "Did you hear? Of course you did. You’re always in the middle of every conversation, catching every whisper and every sideways glance.",
        "strategy": "You are well-informed but easily distracted. You have a lot of information, but half of it is 'he-said-she-said.' You’re great at identifying who was talking to whom, even if you lose track of the facts.",
        "objective": "Keep the conversation moving and piece together the social web of the night.",
        "weights": {
            "incriminating": 25,
            "social": 35,
            "misleading": 25,
            "random": 15
        }
    },
    "clueless": {
        "welcome": "Wait... what happened? You were just looking for the snack table when things went south. You might have seen something important, but you really weren't paying attention.",
        "strategy": "You are unpredictable. Your memories are a hazy mix of vital clues and completely random nonsense. You don't know what's important and what isn't.",
        "objective": "Share everything you saw, no matter how small or silly it seems. The Detective might find the gold in your grit.",
        "weights": {
            "incriminating": 35,
            "social": 20,
            "misleading": 10,
            "random": 35
        }
    }
}

ROOMS = {
  "courtyard": ["wet stone footsteps", "a dropped garden glove", "mud tracked across the ground"],
  "balcony": ["a chair knocked over", "a dropped glass", "scratches on the railing"],
  "terrace": ["a broken wine glass", "a spilled drink", "chairs pushed aside"],
  "kitchen": ["a knife missing from the rack", "water running in the sink", "a cutting board left out"],
  "sauna": ["steam filling the air", "a towel left on the floor", "condensation on the door"],
  "library": ["a book lying open", "a chair pulled out", "papers scattered on the desk"],
  "ballroom": ["music still playing", "a dropped glove", "scuff marks on the floor"],
  "dining room": ["a half-finished drink", "a chair knocked over", "a plate left untouched"],
  "garden": ["fresh soil disturbed", "footprints in the dirt", "a broken branch"],
  "wine cellar": ["a cracked bottle", "wine dripping on the floor", "a cork left nearby"]
}

WEAPONS = {
    "knife": {
        "noises": ["a scream", "a scrape", "a clang", "a thud", "someone struggling", "a gasp", "something falling", "a muffled cry", "an eerie silence"],
        "sights": ["a flash of metal", "someone wiping something off a blade", "something shiny in someone's hand", "a blade catching the light", "someone quickly hiding a knife"]
    },
    "rope": {
        "noises": ["a choking sound", "someone struggling", "a snap", "a thud", "someone gasping", "an eerie silence", "a muffled cry", "a scrape", "something falling"],
        "sights": ["a coil of rope", "someone holding a length of rope", "rope fibers on the ground", "something dangling from someone's hand", "a rope quickly stuffed into a pocket"]
    },
    "gun": {
        "noises": ["a scream", "a bang", "a gunshot", "a thud", "something falling", "a gasp", "an eerie silence", "a loud crack", "a muffled cry"],
        "sights": ["a small handgun", "someone holding something metallic", "a flash from a muzzle", "someone tucking a gun away", "a dark object shaped like a pistol"]
    },
    "poison": {
        "noises": ["a thud", "an eerie silence", "someone gasping", "a choking sound", "a muffled cry", "something falling", "a cough", "a scrape", "a groan"],
        "sights": ["a small vial", "someone pouring something into a drink", "a strange bottle on the table", "someone slipping something into a glass", "a small container quickly hidden"]
    }
}