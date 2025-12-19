POWER_LIMIT = 10.0

def criticize(state, chosen):
    critique = {
        "chosen": chosen,
        "best": chosen,
        "regret": 0.0,
        "message": ""
    }

    if state.energy_used > POWER_LIMIT:
        critique["message"] += (
            "⚠ High power usage detected. Consider switching to FAN.\n"
        )

    if state.temperature <= 26 and chosen == "AC":
        critique["best"] = "FAN"
        critique["regret"] = 0.7
        critique["message"] += (
            "🌡 Room already cool. FAN is more efficient now.\n"
        )

    return critique
