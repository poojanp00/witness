def printer(assignments, crime, memories, show_answers, show_type):

    if show_answers:
        print("--- GAME ASSIGNMENTS ---\n")
        for name, data in assignments.items():
            role_label = data["role"].upper()
            print(f"{name.ljust(12)} | Role: {role_label}")
        print()

        print("--- CRIME ---\n")
        print(f"Weapon: {crime['weapon']}, Room: {crime['room']}, Time: {crime['time']}")
        print()

    print("--- PLAYER MEMORIES ---")
    for name in sorted(memories.keys()):
        print(f"\n{name.upper()}")
        for i, memory in enumerate(memories[name], 1):
            if show_type:
                print(f"  {i}. [{memory['type']}] {memory['text']}")
            else:
                print(f"  {i}. {memory['text']}")

    return memories