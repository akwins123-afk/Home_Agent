def step(state, target_temp, occupancy):
    temperature = state["temperature"]
    energy = state["energy_used"]
    ac = state["devices"]["ac"]
    fan = state["devices"]["fan"]

    chosen = "NONE"
    best = "NONE"
    regret = 0.0
    message = None

    # -------------------------------
    # DEVICE EFFECTS
    # -------------------------------
    if ac:
        temperature -= 1.2
        energy += 2.5
        chosen = "AC"

    if fan:
        temperature -= 0.4
        energy += 0.6
        chosen = "FAN" if chosen == "NONE" else "AC+FAN"

    # Clamp temperature
    temperature = round(max(18, temperature), 2)
    energy = round(energy, 2)

    # -------------------------------
    # AI DECISION LOGIC (FIXED)
    # -------------------------------

    # PHASE 1: Too hot → AC best
    if temperature > target_temp + 0.5:
        best = "AC"
        if not ac:
            regret = 5.0
            message = "🔥 It's hot. Ignoring AC wastes comfort and energy."

    # PHASE 2: Target reached → FAN best
    elif temperature <= target_temp:
        best = "FAN"
        if ac:
            regret = 6.5
            message = "❄️ Target reached. AC is now overkill."

    # PHASE 3: Comfortable idle
    else:
        best = "NONE"

    # -------------------------------
    # UPDATE STATE
    # -------------------------------
    state["temperature"] = temperature
    state["energy_used"] = energy

    critique = {
        "chosen": chosen,
        "best": best,
        "regret": regret,
        "message": message,
    }

    return state, critique
