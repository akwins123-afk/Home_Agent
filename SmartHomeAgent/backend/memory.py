_decisions = []
_energy = []
_temperature = []
_notifications = set()  # prevents duplicates


def store_decision(chosen, best, regret):
    _decisions.append({
        "chosen": chosen,
        "best": best,
        "regret": regret
    })


def add_energy(val):
    _energy.append(val)


def add_temperature(val):
    _temperature.append(val)


def add_notification(msg):
    _notifications.add(msg)


def get_notifications():
    return list(_notifications)


def clear_notifications():
    _notifications.clear()


def get_decisions():
    return _decisions
