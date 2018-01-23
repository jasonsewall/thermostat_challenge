class building:
    def __init__(self, temp, eflux, spec_heat):
        self.spec_heat = spec_heat
        self.eflux = eflux
        self.temp = temp
    def extern_flux_tick(self, otemp):
        self.temp += self.eflux * (self.temp - self.otemp)
    def intern_flux_tick(self, ijoules):
        self.temp += ijoules / self.spec_heat

class furnace:
    def __init__(self, jpf):
        self.fuel_burned = 0
        self.jouls_per_fuel = jpf
        self.burnrate_m = 1.0
        self.startup_use = 1.0
        self.running = True
    def turn_on(self, time_m):
        self.on = True
        self.ontime_m = time_m
    def output(self, tick):
        if self.on == True:
            return tick*self.burnrate_m
    def turn_off(self, time_m):
        self.off = True
        self.fuel_burned = self.startup_use + (self.ontime_m - time_m)*self.burnrate

class climate:
    def __init__(self):
        pass

class thermostat:
    def __init__(self, target_temp, building, furnace, climate):
        self.building = building
        self.furnace = furnacae
        self.climate = climate
        self.time = 0
        self.ticksize = (1.0/24.0)/60
        self.building.temp = target_temp
    def tick(self):
        exterior_temp = self.climate.temp(time)
        self.building.extern_flux_tick(exterior_temp)
        if False:
            self.furnace.
