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
│   ├── memories/
│   │   ├── generators.py      # Memory generation functions
│   │   └── engine.py          # Memory type selection & weighting
│   ├── data/
│   │   ├── artifacts.py       # ROLES, WEAPONS, ROOMS data
│   │   └── fragments.py       # Sentence fragments for memory building
│   └── utils/
│       ├── time_utils.py      # Time phrase generation
│       ├── printer.py         # Game output formatting
│       └── test.py            # Testing utilities
```

---

## Core Data Models

### ROLES Dictionary

Each role defines a player's perspective, bias, and memory distribution. Each includes a `persona` field for character flavor.

| Role | Persona | Weights (Inc/Mis/Soc/Rand) | Key Trait |
|------|---------|----------------------------|-----------|
| **detective** | The Keen Observer | 70/20/0/10 | Highly accurate incriminating memories |
| **culprit** | The Master of Puppets | 0/80/0/20 | Master of misleading fabrications |
| **accomplice** | The Loyal Shadow | 10/70/0/20 | Protects culprit with red herrings |
| **lover** | The Devoted Protector | 45/35/0/20 | Biased observations of loved ones |
| **rival** | The Sharp Tongue | 25/55/5/15 | Misremembers to frame enemies |
| **gossip** | The Social Butterfly | 25/10/65/0 | Tracks social interactions obsessively |
| **clueless** | The Accidental Witness | 30/10/25/35 | Random mix of truth and nonsense |

**Weights breakdown:**
- `incriminating`: Truthful memories pointing to the culprit
- `misleading`: False memories sent to confuse the investigation
- `social`: Observations about player interactions & relationships
- `random`: Nonsensical memories about unrelated details

### WEAPONS Dictionary

Weapons with associated sensory clues.

| Weapon | Example Noises | Example Evidence |
|--------|----------------|------------------|
| **knife** | "a scream", "a clang", "someone struggling" | "flash of metal", "someone hiding a knife" |
| **rope** | "choking sound", "a snap", "someone gasping" | "coil of rope", "rope fibers on ground" |
| **gun** | "a bang", "a gunshot", "a loud crack" | "small handgun", "flash from muzzle" |
| **poison** | "a thud", "choking sound", "a cough" | "small vial", "pouring into drink" |

Each weapon has:
- `noises`: Auditory evidence (used in `weapon_noise_memory()`)
- `evidence`: Visual evidence (used in `weapon_evidence_memory()`)

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
- `noises`: Sound-based memories (used in `room_noise_memory()`)
- `evidence`: Visual memories (used in `room_evidence_memory()`)

---

## Memory Generation System

### 4 Memory Types

Players generate 5 personalized memories based on weighted random selection:

1. **Incriminating** - Truthful observations pointing toward the actual crime
2. **Misleading** - False observations pointing toward wrong details
3. **Social** - Observations about player interactions & relationships
4. **Random** - Nonsensical memories about unrelated details

### Memory Generators (`generators.py`)

| Function | Signature | Returns | Memory Prefix |
|----------|-----------|---------|---------------|
| `movement_memory()` | `(crime, guilty, innocent, flag)` | Person moving through locations | `INC_MOV` / `MISL_MOV` |
| `weapon_noise_memory()` | `(crime, flag)` | Auditory weapon evidence | `INC_WPN_NSE` / `MISL_WPN_NSE` |
| `weapon_evidence_memory()` | `(crime, flag)` | Visual weapon evidence | `INC_WPN_EVI` / `MISL_WPN_EVI` |
| `room_noise_memory()` | `(crime, flag)` | Auditory room evidence | `INC_RM_NSE` / `MISL_RM_NSE` |
| `room_evidence_memory()` | `(crime, flag)` | Visual room evidence | `INC_RM_EVI` / `MISL_RM_EVI` |
| `incrim_social_memory()` | `(guilty)` | Guilty parties interacting | `INC_SOC` |
| `lover_social_memory()` | `(lovers)` | Lovers interacting | `LOV_SOC` |
| `mislead_social_memory()` | `(person_a, person_b)` | Innocent parties or solo interactions | `MISL_SOC` |
| `random_memory()` | `()` | Unrelated nonsensical detail | `RAND` |

**Flag meaning:**
- `flag == 1`: Generate incriminating (truthful) memory
- `flag == 0`: Generate misleading (false) memory

**Memory Prefixes:** Each generated memory includes a label showing its type and category (e.g., `INC_MOV:`, `MISL_WPN_EVI:`, `LOV_SOC:`)

### Memory Engine (`engine.py`)

Hierarchical memory generation with weighted category selection:

```
recall_player_memory(crime, guilty, innocent, lovers, weights)
    ↓
weighted_choice(weights) → mem_type (incriminating/misleading/social/random)
    ↓
    ├─ INCRIMINATING (4 equal categories @ 25% each)
    │   ├─ Category 1: WEAPON (25%) → 50/50 Noise or Evidence
    │   │   └─ [weapon_noise_memory(1), weapon_evidence_memory(1)]
    │   ├─ Category 2: ROOM (25%) → 50/50 Noise or Evidence
    │   │   └─ [room_noise_memory(1), room_evidence_memory(1)]
    │   ├─ Category 3: MOVEMENT (25%)
    │   │   └─ movement_memory(guilty, innocent, 1)
    │   └─ Category 4: SOCIAL (25%)
    │       └─ incrim_social_memory(guilty)
    │
    ├─ MISLEADING (4 equal categories @ 25% each)
    │   ├─ Category 1: WEAPON (25%) → 50/50 Noise or Evidence
    │   │   └─ [weapon_noise_memory(0), weapon_evidence_memory(0)]
    │   ├─ Category 2: ROOM (25%) → 50/50 Noise or Evidence
    │   │   └─ [room_noise_memory(0), room_evidence_memory(0)]
    │   ├─ Category 3: MOVEMENT (25%)
    │   │   └─ movement_memory(guilty, innocent, 0)
    │   └─ Category 4: SOCIAL (25%)
    │       └─ mislead_social_memory(innocent[0], innocent[1])
    │
    ├─ SOCIAL (3 weighted categories)
    │   ├─ Category 1: GUILTY (40%)
    │   │   └─ incrim_social_memory(guilty)
    │   ├─ Category 2: LOVERS (40%)
    │   │   └─ lover_social_memory(lovers)
    │   └─ Category 3: INNOCENT (20%)
    │       └─ mislead_social_memory(innocent[0], innocent[1])
    │
    └─ RANDOM (100%)
        └─ random_memory()
```

### 14 Memory Type Probabilities by Role

Each player receives memories distributed across **14 distinct memory types** (with unique function + prefix combinations) based on their role's weights:

| Role | WPN Noise (Inc) | WPN Evid (Inc) | RM Noise (Inc) | RM Evid (Inc) | Mov (Inc) | SOC Guilty (Inc) | WPN Noise (Misl) | WPN Evid (Misl) | RM Noise (Misl) | RM Evid (Misl) | Mov (Misl) | SOC Innocent (Misl) | SOC Guilty | SOC Lovers | SOC Innocent | Random | Role |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Culprit** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 10.00% | 10.00% | 10.00% | 10.00% | 20.00% | 20.00% | 0.00% | 0.00% | 0.00% | 20.00% | **Culprit** |
| **Accomplice** | 1.25% | 1.25% | 1.25% | 1.25% | 2.50% | 2.50% | 8.75% | 8.75% | 8.75% | 8.75% | 17.50% | 17.50% | 0.00% | 0.00% | 0.00% | 20.00% | **Accomplice** |
| **Detective** | 8.75% | 8.75% | 8.75% | 8.75% | 17.50% | 17.50% | 2.50% | 2.50% | 2.50% | 2.50% | 5.00% | 5.00% | 0.00% | 0.00% | 0.00% | 10.00% | **Detective** |
| **Lover** | 5.62% | 5.62% | 5.62% | 5.62% | 11.25% | 11.25% | 4.38% | 4.38% | 4.38% | 4.38% | 8.75% | 8.75% | 0.00% | 0.00% | 0.00% | 20.00% | **Lover** |
| **Rival** | 3.12% | 3.12% | 3.12% | 3.12% | 6.25% | 6.25% | 6.88% | 6.88% | 6.88% | 6.88% | 13.75% | 13.75% | 2.00% | 2.00% | 1.00% | 15.00% | **Rival** |
| **Gossip** | 3.12% | 3.12% | 3.12% | 3.12% | 6.25% | 6.25% | 1.25% | 1.25% | 1.25% | 1.25% | 2.50% | 2.50% | 26.00% | 26.00% | 13.00% | 0.00% | **Gossip** |
| **Clueless** | 3.75% | 3.75% | 3.75% | 3.75% | 7.50% | 7.50% | 1.25% | 1.25% | 1.25% | 1.25% | 2.50% | 2.50% | 10.00% | 10.00% | 5.00% | 35.00% | **Clueless** |
| **AVG** | **3.66%** | **3.66%** | **3.66%** | **3.66%** | **7.32%** | **7.32%** | **5.00%** | **5.00%** | **5.00%** | **5.00%** | **10.00%** | **10.00%** | **5.43%** | **5.43%** | **2.71%** | **17.14%** | **100%** |

**Legend:**
- **(Inc)** = Generated from Incriminating memory type
- **(Misl)** = Generated from Misleading memory type
- **Social Guilty/Lovers/Innocent** = Generated from Social memory type

### Example of Each 14 Memory Type

| # | Memory Type | Prefix | Example |
|---|---|---|---|
| 1 | Weapon Noise (Incriminating) | `INC_WPN_NSE` | "I heard a thud moments after 21:55." |
| 2 | Weapon Evidence (Incriminating) | `INC_WPN_EVI` | "I saw someone slipping something into a glass near the ballroom." |
| 3 | Room Noise (Incriminating) | `INC_RM_NSE` | "I heard a muffled gasp." |
| 4 | Room Evidence (Incriminating) | `INC_RM_EVI` | "I noticed scuff marks on the floor precisely at 21:55." |
| 5 | Movement (Incriminating) | `INC_MOV` | "I noticed Diya leaving the area at 21:55." |
| 6 | Weapon Noise (Misleading) | `MISL_WPN_NSE` | "I heard a loud bang in the ballroom." |
| 7 | Weapon Evidence (Misleading) | `MISL_WPN_EVI` | "I saw a flash from a muzzle moments before 21:50." |
| 8 | Room Noise (Misleading) | `MISL_RM_NSE` | "I heard a chair scraping against the floor." |
| 9 | Room Evidence (Misleading) | `MISL_RM_EVI` | "I noticed broken glass in the garden." |
| 10 | Movement (Misleading) | `MISL_MOV` | "I caught a glimpse of someone standing near the room not long after 21:52." |
| 11 | Social - Guilty | `INC_SOC` | "Baa didn't want anyone noticing them with Diya sometime in the night." |
| 12 | Social - Lovers | `LOV_SOC` | "Sarah and Tom were whispering together just before the incident." |
| 13 | Social - Innocent | `MISL_SOC` | "Shalini seemed to be nursing a very stiff drink." |
| 14 | Random | `RAND` | "I heard laughter from another room later in the evening." |

**Note:** Social memory types (Guilty, Lovers, Innocent) can appear from both their source memory type AND the Social memory type category, so they have multiple pathways to selection, but only 1 unique prefix + function per type.

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

## Recent Changes & Refactoring

### Terminology: "Clue" → "Memory"
- Renamed all terminology from "clue" to "memory" throughout codebase
- File path: `game/clues/` → `game/memories/`
- Function imports updated in `main.py`
- Variable naming: `player_clues` → `player_memories`

### Role Data Structure
- Added `persona` field to each role (e.g., "The Keen Observer", "The Master of Puppets")
- Updated Detective weights from `80/20/0/10` to **`70/20/0/10`** to sum to 100%
- All weights now properly sum to 100%

### ROOMS/WEAPONS Structure Unification
- **ROOMS:** Transformed from flat list to nested dict with `noises` and `evidence` fields
- Matches WEAPONS structure exactly (both have `noises` and `evidence` keys)
- **WEAPONS:** Renamed `sights` field to `evidence` for consistency
- All generator functions updated to reference the new structure

### Memory Generator Functions
- **Split social_memory():** Original single function split into 3 specialized functions:
  - `incrim_social_memory(guilty)` - Guilty party interactions
  - `lover_social_memory(lovers)` - Lover interactions
  - `mislead_social_memory(person_a, person_b)` - Innocent/other interactions
- Fixed `random.shuffle()` bug: Changed to `random.sample()` for proper list sampling
- Added memory output prefixes for clarity:
  - `INC_MOV`, `INC_WPN_NSE`, `INC_WPN_EVI`, `INC_RM_NSE`, `INC_RM_EVI`, `INC_SOC` (Incriminating)
  - `MISL_MOV`, `MISL_WPN_NSE`, `MISL_WPN_EVI`, `MISL_RM_NSE`, `MISL_RM_EVI`, `MISL_SOC` (Misleading)
  - `LOV_SOC` (Lover), `RAND` (Random)

### Hierarchical Memory Generation
- **Incriminating & Misleading:** Refactored to 4 equal categories (25% each):
  1. **Weapon** (25%) → 50/50 split between Noise (12.5%) and Evidence (12.5%)
  2. **Room** (25%) → 50/50 split between Noise (12.5%) and Evidence (12.5%)
  3. **Movement** (25%)
  4. **Social** (25%) - Guilty for incriminating, Innocent for misleading

- **Social Memory Type:** 3-way weighted split (40/40/20):
  1. **Guilty Interactions** (40%)
  2. **Lover Interactions** (40%)
  3. **Innocent Interactions** (20%)

- **Probability Movement:** Social memory type branching logic moved from generator function to engine level, matching incriminating/misleading pattern

### Variable Naming
- Standardized local variables to use `mem`/`mems` shorthand instead of `clue`/`clues`
- Consistent naming across all memory generators and engine

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
    "INC_WPN_NSE: I heard a scream near the kitchen.",
    "INC_WPN_EVI: I saw a flash of metal 2 minutes before midnight.",
    "INC_RM_EVI: I noticed a knife missing from the rack.",
    "MISL_MOV: I saw Sarah running through the library 3 minutes before the witching hour.",
    "RAND: I felt a sudden chill around midnight."
  ],
  "Detective_memories": [
    "INC_WPN_EVI: I saw someone hiding a knife.",
    "INC_RM_NSE: I heard strange sounds in the kitchen around 11:47 PM.",
    "INC_MOV: I observed the culprit near the kitchen.",
    "LOV_SOC: Sarah and Tom were whispering together just before the incident.",
    "MISL_WPN_NSE: I heard a gunshot near the library."
  ],
  "Culprit_memories": [
    "MISL_WPN_NSE: I heard a loud bang in the ballroom.",
    "MISL_RM_EVI: I noticed broken glass in the garden.",
    "MISL_MOV: I saw the detective running toward the wine cellar.",
    "MISL_WPN_EVI: I saw a rope in someone's hand.",
    "RAND: The music seemed to stop at exactly midnight."
  ]
}
```

**Memory Format:** Each memory includes a prefix label indicating its type and category (e.g., `INC_WPN_EVI:` = Incriminating, Weapon, Evidence).

---

## Next Steps

- [ ] Implement web UI (index.html → game state/display)
- [ ] Add voting/accusation mechanics
- [ ] Implement reveal and win conditions
- [ ] Add game persistence (JSON file storage)
- [ ] Create multiplayer networking (WebSocket)
