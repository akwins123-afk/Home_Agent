class HomeState:
    def __init__(self):
        self.temperature = 31.0
        self.target_temperature = 26.0
        self.occupancy = 1

        self.energy_used = 0.0
        self.energy_limit = 8.0  # kWh per day

        self.devices = {
            "ac": False,
            "fan": False
        }

        self.ac_runtime = 0  # minutes

    def comfort_score(self):
        diff = abs(self.temperature - self.target_temperature)
        return max(0, 100 - diff * 18)

    def snapshot(self):
        return {
            "temperature": round(self.temperature, 2),
            "target_temperature": self.target_temperature,
            "occupancy": self.occupancy,
            "energy_used": round(self.energy_used, 2),
            "energy_limit": self.energy_limit,
            "comfort": round(self.comfort_score(), 1),
            "devices": self.devices
        }
