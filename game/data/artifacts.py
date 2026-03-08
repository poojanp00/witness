# -------------------------------
# ARTIFACTS
# -------------------------------
# File contains the artifacts and their details
# -------------------------------

ROLES = {
    "culprit": {
        "persona": "The Master of Puppets",
        "welcome": "The deed is done, and the adrenaline is fading. Now, the real work begins. You must blend in, fade into the background, and lead this pack of hounds on a wild goose chase.",
        "strategy": "You are the architect of confusion. Most of your memories are calculated fabrications designed to frame others. You rarely trip over your own story.",
        "objective": "Survive the votes. Deflect suspicion toward the Rivals or the innocent guests.",
        "weights": {
            "incriminating": 0,
            "social": 0,
            "misleading": 80,
            "random": 20
        }
    },
    "accomplice": {
        "persona": "The Loyal Shadow",
        "welcome": "You saw what happened, and you’ve made your choice. You aren’t the one with blood on your hands, but you’re the one holding the towel. If they go down, you go down.",
        "strategy": "You are a distraction expert. You remember many things that didn’t actually happen, specifically to protect the Culprit. However, guilt is a heavy burden, and a true slip-up might occur.",
        "objective": "Keep the heat off the Culprit by flooding the conversation with red herrings.",
        "weights": {
            "incriminating": 10,
            "social": 0,
            "misleading": 70,
            "random": 20
        }
    },
    "detective": {
        "persona": "The Keen Observer",
        "welcome": "The room is full of noise, but you only hear the discord. Your mind is a steel trap, and your eyes never miss a detail that others overlook.",
        "strategy": "You are the most reliable person in this room. Your memories are highly accurate and often pinpoint the specific location, weapon, or movements of the culprit.",
        "objective": "Filter out the gossip and lead the group toward the truth—but be careful, the culprit knows you are the biggest threat.",
        "weights": {
            "incriminating": 70,
            "social": 0,
            "misleading": 20,
            "random": 10
        }
    },
    "lover": {
        "persona": "The Devoted Protector",
        "welcome": "In a house full of strangers, you only have eyes for one person. Your heart is leading your head tonight, and you are fiercely protective of your inner circle.",
        "strategy": "You are observant but biased. You pay close attention to the people you care about, which gives you good insight, but you might unintentionally ignore the truth if it hurts someone you love.",
        "objective": "Share what you know, but decide for yourself who is worth protecting.",
        "weights": {
            "incriminating": 45,
            "social": 0,
            "misleading": 35,
            "random": 20
        }
    },
    "rival": {
        "persona": "The Sharp Tongue",
        "welcome": "You didn’t come here to make friends. Everyone has a secret, and you’re more than happy to expose them—especially if it makes your enemies look guilty.",
        "strategy": "You are cunning and chaotic. You remember a mix of truth and lies, often leaning toward ‘misremembering’ things that make your rivals look suspicious.",
        "objective": "Use the chaos to settle old scores, even if it means the real killer walks free.",
        "weights": {
            "incriminating": 25,
            "social": 5,
            "misleading": 55,
            "random": 15
        }
    },
    "gossip": {
        "persona": "The Social Butterfly",
        "welcome": "Did you hear? Of course you did. You’re always in the middle of every conversation, catching every whisper and every sideways glance.",
        "strategy": "You are well-informed but easily distracted. You have a lot of information, but half of it is ‘he-said-she-said.’ You’re great at identifying who was talking to whom, even if you lose track of the facts.",
        "objective": "Keep the conversation moving and piece together the social web of the night.",
        "weights": {
            "incriminating": 25,
            "social": 60,
            "misleading": 10,
            "random": 5
        }
    },
    "clueless": {
        "persona": "The Accidental Witness",
        "welcome": "Wait... what happened? You were just looking for the snack table when things went south. You might have seen something important, but you really weren't paying attention.",
        "strategy": "You are unpredictable. Your memories are a hazy mix of vital truths and completely random nonsense. You don't know what's important and what isn't.",
        "objective": "Share everything you saw, no matter how small or silly it seems. The Detective might find the gold in your grit.",
        "weights": {
            "incriminating": 30,
            "social": 25,
            "misleading": 10,
            "random": 35
        }
    }
}

ROOMS = {
  "courtyard": {
    "noises": ["footsteps on wet stone", "a heavy thud", "the scrape of something being dragged", "muffled voices echoing", "a door slamming in the distance"],
    "evidence": ["wet stone footsteps", "a dropped garden glove", "mud tracked across the ground"]
  },
  "balcony": {
    "noises": ["wind rattling the railing", "a glass shattering", "the squeak of hinges", "a sudden gust", "something scraping metal"],
    "evidence": ["a chair knocked over", "a dropped glass", "scratches on the railing"]
  },
  "terrace": {
    "noises": ["ice crunching underfoot", "a glass clinking", "chairs being moved", "a splash of liquid", "the creak of wood"],
    "evidence": ["a broken wine glass", "a spilled drink", "chairs pushed aside"]
  },
  "kitchen": {
    "noises": ["a knife being pulled from a rack", "water rushing from the tap", "a cutting board scraping", "a drawer slamming", "the clink of utensils"],
    "evidence": ["a knife missing from the rack", "water running in the sink", "a cutting board left out"]
  },
  "sauna": {
    "noises": ["steam hissing", "a towel being thrown", "the splash of water on hot rocks", "heavy breathing", "a door opening abruptly"],
    "evidence": ["steam filling the air", "a towel left on the floor", "condensation on the door"]
  },
  "library": {
    "noises": ["pages rustling", "a chair scraping against the floor", "a book falling", "papers shuffling", "the creak of the bookcase"],
    "evidence": ["a book lying open", "a chair pulled out", "papers scattered on the desk"]
  },
  "ballroom": {
    "noises": ["the scratch of the record needle", "music stopping abruptly", "footsteps on the polished floor", "a glove dropping", "a muffled gasp"],
    "evidence": ["music still playing", "a dropped glove", "scuff marks on the floor"]
  },
  "dining room": {
    "noises": ["a bottle clanking", "a chair being pulled back", "ice clinking", "a plate clattering", "a thud"],
    "evidence": ["a half-finished drink", "a chair knocked over", "a plate left untouched"]
  },
  "garden": {
    "noises": ["footsteps on gravel", "branches snapping", "soil being disturbed", "a heavy thud against earth", "rustling in the shrubs"],
    "evidence": ["fresh soil disturbed", "footprints in the dirt", "a broken branch"]
  },
  "wine cellar": {
    "noises": ["a bottle clanking", "liquid dripping", "the cork popping", "footsteps echoing", "a thud"],
    "evidence": ["a cracked bottle", "wine dripping on the floor", "a cork left nearby"]
  }
}

WEAPONS = {
    "knife": {
        "noises": ["a scream", "a scrape", "a clang", "a thud", "someone struggling", "a gasp", "something falling", "a muffled cry", "an eerie silence"],
        "evidence": ["a flash of metal", "someone wiping something off a blade", "something shiny in someone's hand", "a blade catching the light", "someone quickly hiding a knife"]
    },
    "rope": {
        "noises": ["a choking sound", "someone struggling", "a snap", "a thud", "someone gasping", "an eerie silence", "a muffled cry", "a scrape", "something falling"],
        "evidence": ["a coil of rope", "someone holding a length of rope", "rope fibers on the ground", "something dangling from someone's hand", "a rope quickly stuffed into a pocket"]
    },
    "gun": {
        "noises": ["a scream", "a bang", "a gunshot", "a thud", "something falling", "a gasp", "an eerie silence", "a loud crack", "a muffled cry"],
        "evidence": ["a small handgun", "someone holding something metallic", "a flash from a muzzle", "someone tucking a gun away", "a dark object shaped like a pistol"]
    },
    "poison": {
        "noises": ["a thud", "an eerie silence", "someone gasping", "a choking sound", "a muffled cry", "something falling", "a cough", "a scrape", "a groan"],
        "evidence": ["a small vial", "someone pouring something into a drink", "a strange bottle on the table", "someone slipping something into a glass", "a small container quickly hidden"]
    }
}


LOCATIONS = {
    "mudroom": {
        "evidence": [
            "a damp wool glove",
            "a pile of melting slush",
            "a salt-stained rug",
            "a wet floor mat"
        ],
        "noises": [
            "the heavy oak door slamming shut",
            "the rhythmic stomping of snow off boots",
            "the sharp jingle of a heavy key ring",
            "the rustle of a stiff, frozen parka"
        ]
    },
    "lounge": {
        "evidence": [
            "a glass with a single ice cube",
            "a sheepskin rug",
            "a single extinguished match on the floor",
            "a book left face-down"
        ],
        "noises": [
            "the soft, melodic clink of ice in glass",
            "the violent crackle of a dying fire",
            "the muffled rustle of a heavy wool rug",
            "the low hum of a record player reaching its end"
        ]
    },
    "Loft Library": {
        "evidence": [
            "a leather-bound book sitting crooked on the shelf",
            "a reading lamp knocked slightly off-center",
            "a pair of spectacles abandoned on a side table",
            "a faint smudge in the layer of dust on the railing"
        ],
        "noises": [
            "a single, sharp creak from a floorboard above",
            "the distinctive 'snap' of a book being closed",
            "a series of muffled, urgent whispers",
            "the sliding of a heavy ladder across the wood"
        ]
    },
    "sauna": {
        "evidence": [
            "thick condensation",
            "a damp towel",
            "a small puddle",
            "the lingering, sharp scent of eucalyptus oil"
        ],
        "noises": [
            "the splash of a wooden bucket hitting the floor",
            "a heavy, wet thud muffled by the steam",
            "a sharp intake of breath followed by a cough",
            "the hiss of water hitting hot volcanic rocks"
        ]
    },
    "Balcony": {
        "evidence": [
            "fresh scratches on the frosted wooden railing",
            "a silver lighter dropped near the edge",
            "a shattered wine glass stem caught in the floor-slats",
            "a thin layer of snow blown inward by a gust"
        ],
        "noises": [
            "the mournful whistle of wind through the balcony slats",
            "the heavy 'shush' of the sliding glass door",
            "a sharp, rhythmic tapping against the exterior glass",
            "the rustle of a heavy winter coat against wood"
        ]
    },
    "Scandi-Kitchen": {
        "evidence": [
            "a half-peeled apple turning brown on the counter",
            "a heavy cutting board with a fresh, deep notch",
            "the faucet dripping steadily into the stone sink",
            "a jar of expensive spices left without its lid"
        ],
        "noises": [
            "a rhythmic, muffled chopping sound",
            "the distinctive metallic 'shush' of a blade",
            "the heavy clatter of a pot on a stone counter",
            "the click of a gas stove being turned off"
        ]
    },
    "Fire Pit": {
        "evidence": [
            "a charred log kicked out of the stone circle",
            "a dusting of grey ash over the surrounding snow",
            "a forgotten metal thermos half-buried in a drift",
            "heavy indents in the frozen ground from someone sitting"
        ],
        "noises": [
            "the sharp, sudden pop of a burning ember",
            "the heavy, dead thud of a log being dropped",
            "the crunch of frozen earth under a heavy weight",
            "the distant, hollow hoot of an owl in the pines"
        ]
    }
}