#!/usr/bin/env python3
"""
Calculate and regenerate the 14 Memory Type Probabilities table in README.md

This script automatically calculates memory type probabilities for each role based on
weights in game/data/artifacts.py, then updates the README with a fresh table.

Usage:
    python scripts/calculate_memory_probabilities.py

The 14 memory types are derived from the hierarchical generation system:
- Incriminating: 4 categories (Weapon Noise, Weapon Evidence, Room Noise, Room Evidence, Movement, Social Guilty)
- Misleading: 4 categories (Weapon Noise, Weapon Evidence, Room Noise, Room Evidence, Movement, Social Innocent)
- Social: 3 weighted categories (Guilty 40%, Lovers 40%, Innocent 20%)
- Random: 1 category (100%)

Probabilities combine cascading percentages through the hierarchy.
Social memory types (Guilty, Innocent) appear from multiple paths and are consolidated.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from game.data.artifacts import ROLES


def calculate_probabilities(roles):
    """
    Calculate probabilities for 14 memory types based on role weights.

    Returns dict: {role_name: {memory_type: probability}}
    """
    memory_types = [
        "WPN Noise Inc",
        "WPN Evid Inc",
        "RM Noise Inc",
        "RM Evid Inc",
        "Mov Inc",
        "SOC Guilty",
        "WPN Noise Misl",
        "WPN Evid Misl",
        "RM Noise Misl",
        "RM Evid Misl",
        "Mov Misl",
        "SOC Innocent",
        "SOC Lovers",
        "Random"
    ]

    probabilities = {}

    for role_name, role_data in roles.items():
        w = role_data["weights"]
        inc = w["incriminating"] / 100.0
        mis = w["misleading"] / 100.0
        soc = w["social"] / 100.0
        rnd = w["random"] / 100.0

        probabilities[role_name] = {
            "WPN Noise Inc": inc * 0.125,
            "WPN Evid Inc": inc * 0.125,
            "RM Noise Inc": inc * 0.125,
            "RM Evid Inc": inc * 0.125,
            "Mov Inc": inc * 0.25,
            "SOC Guilty": (inc * 0.25) + (soc * 0.40),
            "WPN Noise Misl": mis * 0.125,
            "WPN Evid Misl": mis * 0.125,
            "RM Noise Misl": mis * 0.125,
            "RM Evid Misl": mis * 0.125,
            "Mov Misl": mis * 0.25,
            "SOC Innocent": (mis * 0.25) + (soc * 0.20),
            "SOC Lovers": soc * 0.40,
            "Random": rnd * 1.0,
        }

    return probabilities, memory_types


def generate_table(probabilities, memory_types, roles):
    """Generate markdown table for README."""

    # Role order for display
    role_order = list(ROLES.keys())
    role_display = {
        "culprit": "Culprit",
        "accomplice": "Accomplice",
        "detective": "Detective",
        "lover": "Lover",
        "rival": "Rival",
        "gossip": "Gossip",
        "clueless": "Clueless"
    }

    # Start table
    lines = []
    lines.append("| Role | " + " | ".join(memory_types) + " |")
    lines.append("|------|" + "|".join(["---"] * len(memory_types)) + "|")

    # Add each role
    for role_key in role_order:
        role_display_name = role_display.get(role_key, role_key.title())
        row_values = [role_display_name]
        for mem_type in memory_types:
            prob = probabilities[role_key][mem_type]
            row_values.append(f"{prob*100:.1f}%")
        lines.append("| " + " | ".join(row_values) + " |")

    # Calculate averages
    avg_row = ["AVG"]
    for mem_type in memory_types:
        total = sum(probabilities[role_key][mem_type] for role_key in role_order)
        avg = (total / len(role_order)) * 100
        avg_row.append(f"{avg:.1f}%")
    lines.append("| " + " | ".join(avg_row) + " |")

    return "\n".join(lines)


def update_readme(table_content):
    """Update README.md with the new table."""
    readme_path = Path(__file__).parent.parent / "readme.md"

    with open(readme_path, "r") as f:
        content = f.read()

    # Find the section and replace
    start_marker = "## 14 Memory Type Probabilities by Role"
    end_marker = "## Memory Engine"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find section markers in README.md")
        return False

    # Extract text between markers
    before = content[:start_idx + len(start_marker)]
    after = content[end_idx:]

    # Create new content
    new_content = before + "\n\n" + table_content + "\n\n" + after

    with open(readme_path, "w") as f:
        f.write(new_content)

    return True


if __name__ == "__main__":
    probs, mem_types = calculate_probabilities(ROLES)
    table = generate_table(probs, mem_types, ROLES)

    print("Generated Memory Probability Table:")
    print("=" * 120)
    print(table)
    print("=" * 120)

    if update_readme(table):
        print("\n✓ README.md updated successfully!")
    else:
        print("\n✗ Failed to update README.md")
