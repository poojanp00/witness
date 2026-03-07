# -------------------------------
# ROLE-TO-CLUE-TYPE WEIGHTS
# -------------------------------

weights = {
    "detective": {"incriminating":50,"social":20,"misleading":20,"random":10},
    "culprit": {"incriminating":5,"social":20,"misleading":55,"random":15},
    "accomplice": {"incriminating":10,"social":35,"misleading":50,"random":5},
    "lover": {"incriminating":30,"social":40,"misleading":15,"random":15},
    "rival": {"incriminating":25,"social":15,"misleading":45,"random":15},
    "gossip": {"incriminating":25,"social":35,"misleading":25,"random":15},
    "clueless": {"incriminating":35,"social":20,"misleading":10,"random":35}
}