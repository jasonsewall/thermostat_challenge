Thermostat
==========
Jason Sewall

jasonsewall@gmail.com

January 2018

## Quick start

This is a thermostat control example. It models a simple building with a heating system and a varying external climate, and tries to heat the building.

To run it, you need Python installed (see below). From a command prompt with the Python runtime in your path, you can type:

    $ python thermostat.py

And it should print out many lines showing the state of the system over the course of an hour, and summarize things by showing the average temperature of the building and the used fuel.

## Introduction

This aims to show some basic programming and object orientation. There are no dependencies other than Python 3

### License

This is licensed with the permissive Apache License 2.0. See the LICENSE-2.0 file in the root of the distribution for details.

## Installation

In Windows, I recommend [Anaconda][https://www.anaconda.com/download/#windows].

## Overview

There are four classes in this example: `building`, `furnace`, `climate`, and `thermostat`. There is a single free function, `run`, that drives the simulation.

The classes themselves are fairly well-documented in the code, and you can say (from a *Python* prompt, i.e. `python -i thermostat.py`) `help(<class-name>)` to read some of the documentation (or you can just look at the source.)

The `thermostat` class performs timestep `ticks` that look up the external temperature from the `climate`, then uses that to model the building's heat exchange with the climate. Then, furnace output is applied to the building, and finally the thermostat uses available information to decide if the furnace should be turned on or off.

There are a lot of parameters here to play with, including how the furnace works, how the climate behaves, and the thermal properties of the building. The main thing I wanted to demonstrate with this is a simple controller model with the thermostat itself. A poor thermostat (like the example one here) will waste fuel or fail to heat the house properly.

## Challenge

The `thermostat` class has a `thermo_state` method that is called each time tick. It can look at information in the system---`building.temp` might be a good place to start---to decide if the furnace should be turned on or off. See if you can get it to stop failing the temperature test, and then see how good you can make the fuel usage.

One thing to note is that the furnace has a built-in startup cost, meaning that it can be wasteful to switch it on and off repeatedly.

## Other projects

There are a lot of things you can do with this project. Here are some ideas:

- Changing ticksize. Real thermostats have effectively continuous simulation, while we're using 60s ticks. We can do 1s ticks and even smaller, and see how it changes the simulation.
- Plot temperatures: Python has lots of libraries that let you make nice graphs. We could plot temperatures over time and see how it looks.
- More sophisticated climate models
- More sophisticated building models (multiple zones?)
- Different furnace types

## Known issues

No known issues yet!
