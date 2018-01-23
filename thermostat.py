# Copyright 2018 Jason Sewall (jasonsewall@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

class building:
    """A simple model of a building.
       The building's average temperature is 'temp' (in Celcius).
       The transfers heat to/from the outside at a rate of eflux (per second).
       The specific heat of the building is spec_heat."""
    def __init__(self, temp, eflux, spec_heat):
        """Initialize temp, flux value, and specific heat."""
        self.spec_heat = spec_heat
        self.eflux = eflux
        self.temp = temp
    def extern_flux_tick(self, otemp, tick):
        """Exchange heat with external temperature otemp for 'tick' seconds."""
        self.temp -= self.eflux * (self.temp - otemp) * tick
    def intern_flux_tick(self, ijoules):
        """Apply heat ijoules heat from from furnace to building."""
        self.temp += ijoules / self.spec_heat

class furnace:
    """A furnace class.
       Can be 'on' or 'off' (on == True, on == False).
       Keeps track of amount of burned fuel.
       When on, burns fuel at a rate of 'burnrate_s' units per second.
       Each unit of fuel burned produces 'joules per_fuel' joules.
       Startup_us is 'wasted' fuel each time furnace is turned on."""
    def __init__(self, jpf):
        """Initialize furnace model.
           Starts 'off'. Some defaults applied."""
        self.fuel_burned = 0
        self.joules_per_fuel = jpf
        self.burnrate_s = 1.0
        self.startup_use = 1.0
        self.on = False
        self.ontime_s = None
    def turn_on(self, time_s):
        """Turn on the furnace, if not on. Keep track of switch-on time."""
        if not self.on:
            self.on = True
            self.ontime_s = time_s
    def output(self, tick):
        """Report heat output. Zero if off, otherwise constant output"""
        if self.on == True:
            return tick*self.burnrate_s*self.joules_per_fuel
        else:
            return 0.0
    def turn_off(self, time_s):
        """If on, turn off furnace.
           Record total amount of fuel burned."""
        if self.on:
            self.fuel_burned += self.startup_use + (time_s - self.ontime_s)*self.burnrate_s
            self.on = False

class climate:
    """A simple model of a climate that reports temperature as function of time."""
    def __init__(self):
        """Simple 24 hour model that has 6 hours into a day be the lowest temp (-10 C) and repeated with a sinusoidal period over 24 hours."""
        self.min_time = 6.0*60.0*60.0
        self.min_temp = -10.0
        self.max_temp = 10.0
        self.period = 60.0*60.0*24.0
    def temp(self, time):
        """Transform a simple sine wave into our 24-hour temperature model."""
        self.amplitude = (self.max_temp - self.min_temp)
        self.offset = (self.max_temp + self.min_temp)*0.5
        self.phase = self.min_time
        self.scale = 2*math.pi/self.period
        return self.offset + self.amplitude*0.5*math.sin(math.pi*0.5 + self.scale*(self.phase + time))

class thermostat:
    """Unifying thermostat model.
       Has a target temperature to achieve.
       Accepts a building, furnace, and climate to work with.
       Applies thermal model and controls on/off of furnace."""
    def __init__(self, target_temp, building, furnace, climate):
        """Initialize a thermostat. Pick ticksize of 1 minute (60s)."""
        self.building = building
        self.furnace = furnace
        self.climate = climate
        self.time = 0
        self.ticksize_s = 60.0
    def tick(self):
        """Using constant ticksize, get exterior temp and exchange heat between climate and building.
           Apply furnace output.
           Check to see if furnace needs to toggled.
           Advance time."""
        dt = self.ticksize_s
        exterior_temp = self.climate.temp(self.time)
        self.building.extern_flux_tick(exterior_temp, dt)
        furn_output = self.furnace.output(dt)
        self.building.intern_flux_tick(furn_output)
        if False:
            self.furnace.turn_on(self.time)
        else:
            self.furnace.turn_off(self.time)
        self.time += dt

def run(end_t):
    """Actually run with some dummy parameters"""
    b = building(20, 1e-4, 1e6)
    f = furnace(1e4)
    c = climate()
    thermo = thermostat(20, b, f, c)
    while thermo.time < end_t:
        outside_temp = c.temp(thermo.time)
        thermo.tick()
        if f.on:
            furnace_status = "on"
        else:
            furnace_status = "off"
        print("min: " + str(thermo.time/60.0) + " outside: " + str(outside_temp) + " inside:" +  str(b.temp) + " furnace: " + furnace_status)
    f.turn_off(thermo.time)
    print("Used fuel: " + str(f.fuel_burned))
