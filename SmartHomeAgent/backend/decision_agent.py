def choose_action(current_temp, target_temp, energy_used):
    """
    Rule-based decision logic with regret awareness
    """

    # Temperature error
    delta = current_temp - target_temp

    # ---------- HARD RULES ----------
    # Too hot → AC is mandatory
    if delta > 1.0:
        chosen = "AC"
        best = "AC"
        regret = 0.0
        return chosen, best, regret

    # Near target → FAN is best
    if 0.0 < delta <= 0.5:
        chosen = "AC" if energy_used < 2.0 else "FAN"
        best = "FAN"

        regret = round(abs(energy_used - 0.3), 2)
        return chosen, best, regret

    # Comfortable or cold → turn things off
    if delta <= 0:
        chosen = "NONE"
        best = "NONE"
        regret = 0.0
        return chosen, best, regret

    # ---------- FALLBACK ----------
    return "NONE", "NONE", 0.0
