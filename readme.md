# Witness: A Deduction Party Game

A social deduction game where players take on different roles to uncover clues about a "crime" based on their character's perspective and biases. Each player generates personalized clues matching their role's personality and objectives.

---

## Game Overview

**Setup:** 7-10 players are assigned random roles. A secret crime (weapon, room, time) is generated and hidden from all players.

**Objective:** Players share memories from their perspective to deduce the crime details. Some roles are truthful; others deliberately mislead.

**Outcome:** Vote on who the culprit is. Culprit and accomplice win if the guilty party is acquitted.

---

## File Structure

```
witness/
├── main.py                    # Game initialization & role assignment
├── index.html                 # Web UI (placeholder)
├── game/
│   ├── clues/
│   │   ├── generators.py      # Clue generation functions
│   │   └── engine.py          # Clue type selection & weighting
│   ├── data/
│   │   ├── artifacts.py       # ROLES, WEAPONS, ROOMS data
│   │   └── fragments.py       # Sentence fragments for clue building
│   └── utils/
│       ├── time_utils.py      # Time phrase generation
│       ├── printer.py         # Game output formatting
│       └── test.py            # Testing utilities
```

---

## Core Data Models

### ROLES Dictionary

Each role defines a player's perspective, bias, and clue distribution. Updated to include `persona` field.

| Role | Persona | Weights (Inc/Soc/Mis/Rand) | Key Trait |
|------|---------|----------------------------|-----------|
| **detective** | The Keen Observer | 50/20/20/10 | Provides accurate incriminating clues |
| **culprit** | The Master of Puppets | 0/25/55/15 | Generates misleading fabrications |
| **accomplice** | The Loyal Shadow | 10/35/50/5 | Protects culprit with red herrings |
| **lover** | The Devoted Protector | 30/40/15/15 | Biased toward protecting loved ones |
| **rival** | The Sharp Tongue | 25/15/45/15 | Misremembers to frame enemies |
| **gossip** | The Social Butterfly | 25/35/25/15 | Tracks social interactions |
| **clueless** | The Accidental Witness | 35/20/10/35 | Random mix of truth and nonsense |

**Weights breakdown:**
- `incriminating`: Truthful clues pointing to the culprit
- `social`: Observations about who was talking to whom
- `misleading`: False clues sent to confuse the investigation
- `random`: Nonsensical clues about unrelated details

### WEAPONS Dictionary

Weapons with associated sensory clues.

| Weapon | Example Noises | Example Evidence |
|--------|----------------|------------------|
| **knife** | "a scream", "a clang", "someone struggling" | "flash of metal", "someone hiding a knife" |
| **rope** | "choking sound", "a snap", "someone gasping" | "coil of rope", "rope fibers on ground" |
| **gun** | "a bang", "a gunshot", "a loud crack" | "small handgun", "flash from muzzle" |
| **poison** | "a thud", "choking sound", "a cough" | "small vial", "pouring into drink" |

Each weapon has:
- `noises`: Auditory evidence (used in noise_clue)
- `evidence`: Visual evidence (used in weapon_clue)

### ROOMS Dictionary

Crime scene locations with atmospheric details.

| Room | Example Noises | Example Evidence |
|------|----------------|------------------|
| **courtyard** | "footsteps on wet stone", "heavy thud" | "wet stone footsteps", "dropped garden glove" |
| **kitchen** | "knife pulled from rack", "water rushing" | "knife missing from rack", "cutting board left out" |
| **library** | "pages rustling", "book falling", "whispers" | "book lying open", "papers scattered" |
| **sauna** | "steam hissing", "towel thrown", "water splashing" | "steam filling air", "towel on floor" |
| **balcony** | "wind whistling", "glass shattering", "tapping" | "scratches on railing", "dropped glass" |
| **ballroom** | "record needle scratch", "footsteps on floor" | "dropped glove", "scuff marks" |
| **dining room** | "glass set down hard", "chair pulled back" | "half-finished drink", "chair knocked over" |
| **garden** | "footsteps on gravel", "branches snapping" | "disturbed soil", "footprints in dirt" |
| **terrace** | "ice crunching", "glass clinking", "chairs moving" | "broken wine glass", "spilled drink" |
| **wine cellar** | "bottle shattering", "liquid dripping", "cork popping" | "cracked bottle", "wine dripping" |

Each room has:
- `noises`: Sound-based clues (used in noise_clue)
- `evidence`: Visual clues (used in room_clue)

---

## Clue Generation System

### Memory Types

Players generate 5 personalized memories based on weighted random selection of memory types:

1. **Incriminating** - Truthful clues pointing toward the actual crime
2. **Misleading** - False clues pointing toward wrong details
3. **Social** - Observations about player interactions
4. **Random** - Nonsensical details that don't relate to the crime

### Memory Generators (`generators.py`)

| Function | Returns | Depends On |
|----------|---------|-----------|
| `movement_memory(crime, flag)` | Observation of person moving through locations | SUBJECTS, AREAS, MOVEMENTS |
| `weapon_noise_memory(crime, flag)` | Auditory evidence from WEAPONS | WEAPONS["noises"] |
| `weapon_evidence_memory(crime, flag)` | Visual evidence of weapon | WEAPONS["evidence"] |
| `room_memory(crime, flag)` | Physical evidence in location | ROOMS["evidence"] |
| `social_memory(lovers, guilty, innocent)` | Observation of two players together | LOVER_SOCIAL, GUILTY_SOCIAL, SOCIAL |
| `random_memory()` | Unrelated nonsensical detail | RANDOMS |

**Flag meaning:**
- `flag == 1`: Generate incriminating (truthful) clue
- `flag == 0`: Generate misleading (false) clue

### Memory Engine (`engine.py`)

```
recall_player_memory(crime, guilty, innocent, lovers, weights)
    ↓
weighted_choice(weights) → mem_type (incriminating/misleading/social/random)
    ↓
    ├─ incriminating → [weapon_noise_memory(1), weapon_evidence_memory(1), room_memory(1), movement_memory(1)] → pick 1
    ├─ misleading → [weapon_noise_memory(0), weapon_evidence_memory(0), room_memory(0), movement_memory(0)] → pick 1
    ├─ social → social_memory()
    └─ random → random_memory()
```

---

## Game Flow

### 1. Role Assignment (`main.py`)

```
assign_roles(players)
    ↓
Role Pool: [detective, culprit, accomplice, lover, lover, rival, gossip, accomplice, clueless, clueless]
    ↓
Shuffle & assign to each player
    ↓
Link lovers together
    ↓
Assign rival targets
```

**Role Distribution (default 10 players):**
- 1 Detective
- 1 Culprit
- 2 Accomplices
- 2 Lovers
- 1 Rival
- 1 Gossip
- 2 Clueless

### 2. Crime Generation

```
generate_crime(assignments)
    ↓
culprit: [assigned detective's enemy]
weapon: random from WEAPONS.keys()
room: random from ROOMS.keys()
time: random_time()
```

### 3. Memory Generation

For each player, generate 5 memories:
```
for player in players:
    memories[player] = [
        recall_player_memory(crime, guilty, innocent, lovers, player.weights)
        for _ in range(5)
    ]
```

Each call to `recall_player_memory()` uses the player's role-based weights to decide memory type, then generates a contextually appropriate memory.

---

## Running the Game

```bash
python main.py
```

**Output:**
- Game assignments (player → role mapping)
- Crime details (weapon, room, time)
- Personalized clue lists for each player

---

## Recent Changes

### Persona Field (Roles)
Added `persona` field to each role in ROLES dictionary for more descriptive character naming.

### ROOMS/WEAPONS Structure Unification
- **ROOMS:** Transformed from flat list to nested dict with `noises` and `evidence` fields (matches WEAPONS structure)
- **WEAPONS:** Renamed `sights` field to `evidence` for consistency
- **Generators Updated:** All references to old field names updated in `generators.py`

### Variable Naming Consistency
- `weapon_clue()`: Unified `sight`/`wrong_sight` variables to use consistent `evidence` naming across all clue generators

---

## Example Output

```json
{
  "crime": {
    "culprit": "Poojan",
    "weapon": "knife",
    "room": "kitchen",
    "time": "11:47 PM"
  },
  "Poojan_memories": [
    "I heard a scream near the kitchen.",
    "I saw a flash of metal 2 minutes before midnight.",
    "I noticed a knife missing from the rack.",
    "Someone quickly hiding a knife 3 minutes before the witching hour.",
    "I saw Sarah laughing with Tom at midnight."
  ],
  "Diya_memories": [
    "I noticed fresh soil disturbed in the garden.",
    "I heard footsteps in the library.",
    ...
  ]
}
```

---

## Next Steps

- [ ] Implement web UI (index.html → game state/display)
- [ ] Add voting/accusation mechanics
- [ ] Implement reveal and win conditions
- [ ] Add game persistence (JSON file storage)
- [ ] Create multiplayer networking (WebSocket)
