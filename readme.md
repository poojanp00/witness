# Witness: A Deduction Party Game

A social deduction game where players take on different roles to uncover clues about a "crime" based on their character's perspective and biases. Each player generates personalized memories matching their role's personality and objectives.

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
├── app.py                     # Flask web server
├── run.py                     # Flask launcher
├── SETUP.md                   # Setup & running instructions
├── frontend/
│   └── index.html             # Nordic Noir web UI
├── game/
│   ├── memory/
│   │   ├── generators.py      # Memory generation functions
│   │   └── engine.py          # Memory type selection & weighting
│   ├── data/
│   │   ├── artifacts.py       # ROLES, WEAPONS, ROOMS data
│   │   └── fragments.py       # Sentence fragments for memory building
│   └── utils/
│       ├── time.py            # Time phrase generation
│       ├── printer.py         # Game output formatting
│       └── test.py            # Testing utilities
└── scripts/
    └── calculate_memory_probabilities.py  # Auto-generate probability tables
```

---

## Core Data Models

### ROLES Dictionary

Each role defines a player's perspective, bias, and memory distribution based on their weights.

| Role | Weights (Inc/Mis/Soc/Rand) |
|------|----------------------------|
| **detective** | 70/20/0/10 |
| **culprit** | 0/80/0/20 |
| **accomplice** | 10/70/0/20 |
| **lover** | 45/35/0/20 |
| **rival** | 25/55/5/15 |
| **gossip** | 25/60/5/10 |
| **clueless** | 30/10/25/35 |

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
| **courtyard** | "footsteps on wet stone", "heavy thud" | "wet stone footprints", "dropped garden glove" |
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
| `movement_memory()` | `(crime, role, flag)` | Person moving through locations | `INC_MOV` / `MISL_MOV` |
| `weapon_noise_memory()` | `(crime, role, flag)` | Auditory weapon evidence | `INC_WPN_NSE` / `MISL_WPN_NSE` |
| `weapon_evidence_memory()` | `(crime, role, flag)` | Visual weapon evidence | `INC_WPN_EVI` / `MISL_WPN_EVI` |
| `room_noise_memory()` | `(crime, role, flag)` | Auditory room evidence | `INC_RM_NSE` / `MISL_RM_NSE` |
| `room_evidence_memory()` | `(crime, role, flag)` | Visual room evidence | `INC_RM_EVI` / `MISL_RM_EVI` |
| `incrim_social_memory()` | `(crime, role)` | Guilty parties interacting | `INC_SOC` |
| `lover_social_memory()` | `(crime, role)` | Lovers interacting | `LOV_SOC` |
| `mislead_social_memory()` | `(crime, role)` | Innocent parties or solo interactions | `MISL_SOC` |
| `random_memory()` | `(role)` | Unrelated nonsensical detail | `RAND` |

**Flag meaning:**
- `flag == 1`: Generate incriminating (truthful) memory
- `flag == 0`: Generate misleading (false) memory

**Role-Based Observation Tuning:**
Functions `movement_memory()`, `weapon_evidence_memory()`, and `room_evidence_memory()` now use role-based observation clarity:
- **Detective** → `OBS_CLEAR` (precise: "I distinctly noticed...")
- **Clueless** → `OBS_VAGUE` (uncertain: "I think I saw...")
- **Others** → Mix of both observation types

---

## Memory Engine (`engine.py`)

Hierarchical memory generation with weighted category selection:

```
recall_player_memory(crime, weights, role)
    ↓
weighted_choice(weights) → mem_type (incriminating/misleading/social/random)
    ↓
    ├─ INCRIMINATING (4 equal categories @ 25% each)
    │   ├─ Category 1: WEAPON (25%) → 50/50 Noise or Evidence
    │   │   └─ [weapon_noise_memory(crime, role, 1), weapon_evidence_memory(crime, role, 1)]
    │   ├─ Category 2: ROOM (25%) → 50/50 Noise or Evidence
    │   │   └─ [room_noise_memory(crime, role, 1), room_evidence_memory(crime, role, 1)]
    │   ├─ Category 3: MOVEMENT (25%)
    │   │   └─ movement_memory(crime, role, 1)
    │   └─ Category 4: SOCIAL (25%)
    │       └─ incrim_social_memory(crime, role)
    │
    ├─ MISLEADING (4 equal categories @ 25% each)
    │   ├─ Category 1: WEAPON (25%) → 50/50 Noise or Evidence
    │   │   └─ [weapon_noise_memory(crime, role, 0), weapon_evidence_memory(crime, role, 0)]
    │   ├─ Category 2: ROOM (25%) → 50/50 Noise or Evidence
    │   │   └─ [room_noise_memory(crime, role, 0), room_evidence_memory(crime, role, 0)]
    │   ├─ Category 3: MOVEMENT (25%)
    │   │   └─ movement_memory(crime, role, 0)
    │   └─ Category 4: SOCIAL (25%)
    │       └─ mislead_social_memory(crime, role)
    │
    ├─ SOCIAL (3 weighted categories)
    │   ├─ Category 1: GUILTY (40%)
    │   │   └─ incrim_social_memory(crime, role)
    │   ├─ Category 2: LOVERS (40%)
    │   │   └─ lover_social_memory(crime, role)
    │   └─ Category 3: INNOCENT (20%)
    │       └─ mislead_social_memory(crime, role)
    │
    └─ RANDOM (100%)
        └─ random_memory(role)
```

### 14 Memory Type Probabilities by Role

| Role | WPN Noise Inc | WPN Evid Inc | RM Noise Inc | RM Evid Inc | Mov Inc | SOC Guilty | WPN Noise Misl | WPN Evid Misl | RM Noise Misl | RM Evid Misl | Mov Misl | SOC Innocent | SOC Lovers | Random |
|------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Culprit | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 10.0% | 10.0% | 10.0% | 10.0% | 20.0% | 20.0% | 0.0% | 20.0% |
| Accomplice | 1.2% | 1.2% | 1.2% | 1.2% | 2.5% | 2.5% | 8.8% | 8.8% | 8.8% | 8.8% | 17.5% | 17.5% | 0.0% | 20.0% |
| Detective | 8.8% | 8.8% | 8.8% | 8.8% | 17.5% | 17.5% | 2.5% | 2.5% | 2.5% | 2.5% | 5.0% | 5.0% | 0.0% | 10.0% |
| Lover | 5.6% | 5.6% | 5.6% | 5.6% | 11.2% | 11.2% | 4.4% | 4.4% | 4.4% | 4.4% | 8.8% | 8.8% | 0.0% | 20.0% |
| Rival | 3.1% | 3.1% | 3.1% | 3.1% | 6.2% | 8.2% | 6.9% | 6.9% | 6.9% | 6.9% | 13.8% | 14.8% | 2.0% | 15.0% |
| Gossip | 3.1% | 3.1% | 3.1% | 3.1% | 6.2% | 30.2% | 1.2% | 1.2% | 1.2% | 1.2% | 2.5% | 14.5% | 24.0% | 5.0% |
| Clueless | 3.8% | 3.8% | 3.8% | 3.8% | 7.5% | 17.5% | 1.2% | 1.2% | 1.2% | 1.2% | 2.5% | 7.5% | 10.0% | 35.0% |
| AVG | 3.7% | 3.7% | 3.7% | 3.7% | 7.3% | 12.5% | 5.0% | 5.0% | 5.0% | 5.0% | 10.0% | 12.6% | 5.1% | 17.9% |

---

## Example of Each 14 Memory Type

| # | Memory Type | Prefix | Example |
|---|---|---|---|
| 1 | Weapon Noise (Incriminating) | `INC_WPN_NSE` | "I heard a thud moments after 21:55." |
| 2 | Weapon Evidence (Incriminating) | `INC_WPN_EVI` | "I distinctly noticed someone holding something metallic." |
| 3 | Room Noise (Incriminating) | `INC_RM_NSE` | "I heard a muffled gasp." |
| 4 | Room Evidence (Incriminating) | `INC_RM_EVI` | "I noticed scuff marks on the floor precisely at 21:55." |
| 5 | Movement (Incriminating) | `INC_MOV` | "I distinctly noticed Diya leaving the area at 21:55." |
| 6 | Weapon Noise (Misleading) | `MISL_WPN_NSE` | "I heard a loud bang in the ballroom." |
| 7 | Weapon Evidence (Misleading) | `MISL_WPN_EVI` | "I think I saw a flash from a muzzle moments before 21:50." |
| 8 | Room Noise (Misleading) | `MISL_RM_NSE` | "I heard a chair scraping against the floor." |
| 9 | Room Evidence (Misleading) | `MISL_RM_EVI` | "I think I noticed broken glass in the garden." |
| 10 | Movement (Misleading) | `MISL_MOV` | "I think I caught a glimpse of someone standing near the room." |
| 11 | Social - Guilty | `INC_SOC` | "Baa didn't want anyone noticing them with Diya sometime in the night." |
| 12 | Social - Lovers | `LOV_SOC` | "Sarah and Tom were whispering together just before the incident." |
| 13 | Social - Innocent | `MISL_SOC` | "Shalini seemed to be nursing a very stiff drink." |
| 14 | Random | `RAND` | "I heard laughter from another room later in the evening." |

---

## Game Flow

### 1. Role Assignment (`main.py`)

```
assign_roles(players)
    ↓
Role Pool: [detective, culprit, accomplice, lover, lover, rival, gossip, clueless, clueless]
    ↓
Shuffle & assign to each player
    ↓
Link lovers together
    ↓
Assign rival targets
```

**Default 8 players (Poojan, Diya, Kishan, Shalini, Sonal, Sandeep, Baa, Bronnie):**
- 1 Detective
- 1 Culprit
- 1-2 Accomplices
- 2 Lovers
- 1 Rival
- 1 Gossip
- 1-2 Clueless

### 2. Crime Generation

```
generate_crime(assignments)
    ↓
culprit: Assigned detective's enemy or random culprit
weapon: random from WEAPONS.keys()
room: random from ROOMS.keys()
time: random_time()
guilty: [culprit, accomplices]
innocent: [all other players]
lovers: [lover pairs]
```

### 3. Memory Generation

For each player, generate 5 memories:
```
for player in players:
    memories[player] = [
        recall_player_memory(crime, player.weights, player.role)
        for _ in range(5)
    ]
```

Each call to `recall_player_memory()` uses the player's role-based weights to decide memory type, then generates a contextually appropriate memory using role-aware observation clarity.

---

## Web Frontend

### Architecture

The frontend is a responsive single-page application (SPA) built with:
- **HTML/CSS/JS**: Nordic Noir aesthetic (dark, minimalist)
- **Backend Integration**: Flask REST API
- **Memory Cards**: 3D CSS flip animations

### Key Features

- **Login View**: Players enter their name to join the game
- **Dossier View**: Shows player role and atmospheric flavor text
- **Memory Card Grid**: 5 interactive cards with flip animations
- **Role Descriptions**: Narrative flavor text for each role
- **Responsive Design**: Works on mobile, tablet, and desktop
- **3D Card Flip**: Smooth CSS transitions with border change on flip

### API Endpoints

- `GET /` - Serve frontend (index.html)
- `GET /api/game/initialize` - Initialize new game
- `GET /api/game/player/<name>` - Get player-specific game data
- `GET /api/game/state` - Get current game state with available players

---

## Running the Game

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
source venv/bin/activate
python run.py
```

Server runs on `http://localhost:5000`

### CLI (No Web)

```bash
python main.py
```

Outputs game state with all assignments and memories to terminal.

---

## Recent Changes & Refactoring

### Folder & File Renaming
- `game/memories/` → `game/memory/` (singular form)
- `game/utils/time_utils.py` → `game/utils/time.py`
- All imports updated accordingly

### Function Signature Updates
- All memory generator functions now take `role` as second parameter
- New signature: `generator(crime, role, flag)` instead of `(crime, flag)`
- Enables role-based narrative tuning

### Role-Based Observation Clarity
- `movement_memory()`, `weapon_evidence_memory()`, `room_evidence_memory()` now use:
  - Detective → `OBS_CLEAR` (sharp, precise observations)
  - Clueless → `OBS_VAGUE` (uncertain, blurry memories)
  - Others → Mix of both
- Added new imports: `OBS_CLEAR`, `OBS_VAGUE` from `fragments.py`

### Social Memory Refactoring
- Split original `social_memory()` into 3 specialized functions:
  - `incrim_social_memory(crime, role)` - Guilty party interactions
  - `lover_social_memory(crime, role)` - Lover interactions
  - `mislead_social_memory(crime, role)` - Innocent/other interactions
- Crime dict now contains `guilty`, `innocent`, `lovers` lists

### Time Constant Enforcement
- `TIMES1` (exact timing) only used in `flag == 1` (incriminating) branches
- `TIMES2+TIMES3` (vague/wrong timing) only in `flag == 0` (misleading) branches
- Prevents information leakage through temporal precision

### Web Integration
- Created `app.py` - Flask REST API server with lazy initialization
- Created `run.py` - Simple launcher script
- Created `frontend/index.html` - Nordic Noir-themed web UI
- Lazy game initialization to avoid startup delays

### Crime Dict Consolidation
- Crime object now carries: `culprit`, `weapon`, `room`, `time`, `guilty`, `innocent`, `lovers`
- Eliminates need to pass separate parameters to memory generators
- All data accessible via single `crime` dict

---

## Next Steps

- [ ] Implement voting/accusation mechanics
- [ ] Implement reveal and win conditions
- [ ] Add game persistence (JSON file storage)
- [ ] Create multiplayer networking (WebSocket)
- [ ] Add game history and leaderboards
