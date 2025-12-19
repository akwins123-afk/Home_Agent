def apply_ac(state):
    state["devices"]["ac"] = True
    state["devices"]["fan"] = False


def apply_fan(state):
    state["devices"]["fan"] = True
    state["devices"]["ac"] = False


def turn_all_off(state):
    state["devices"]["ac"] = False
    state["devices"]["fan"] = False
