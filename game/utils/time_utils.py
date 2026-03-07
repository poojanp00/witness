from datetime import datetime, timedelta
import random

# -----------------------------
# TIME GENERATION
# -----------------------------
# This function generates random times for clues.
# -----------------------------
def random_time():
    base = datetime.strptime("21:50","%H:%M")
    offset = random.randint(0,10)
    t = base + timedelta(minutes=offset)
    return t.strftime("%H:%M")
