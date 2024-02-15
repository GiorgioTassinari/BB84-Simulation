"""
This module contains functions to launch the simulation multiple times
to find and graph some values
"""
import os
import sys
import matplotlib.pyplot as plt
import simulation

NUMBER_OF_RUNS = 5
PARTICLE_NUMBER_UPPER_RANGE = 100

failure_rates = []
number_of_particles = list(range(1,PARTICLE_NUMBER_UPPER_RANGE))

class HiddenPrints:
    """Class to hide printing from all the simulation runs"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def simulate_fixed(number_of_runs, particles):
    """
    Function that runs the simulation a certain number of times, whith
    eavesdropping turned on.

    Parameters
    ----------
        number_of_runs : int
            The number of times the simulation will run
        particles : int
            The number of particles uses in each run of the simulation
    Returns
    -------
        failure_rate : float
            The rate of eavesdropping/failures detected by the different
            runs of the simulation over the total number of runs done.
    """
    number_of_detections = 0
    for _ in range(number_of_runs):
        with HiddenPrints(): #mute the prints of the simulation
            if simulation.run(n=particles, eavesdropping=True):
                number_of_detections += 1
    failure_rate=number_of_detections/number_of_runs
    return failure_rate

for i,number in enumerate(number_of_particles):
    failure_rates.append(simulate_fixed(NUMBER_OF_RUNS,number))
    print(f"Simulation is at {i} out of {len(number_of_particles)}",end="\r")

def plotting():
    """
    Function that plots the chosen number of paricles on the x axis and
    the detection rate of problems in the key on the y axis.
    """
    p = plt.figure(figsize=(12,9))
    plt.scatter(number_of_particles, failure_rates, s=40)
    plt.xlabel("Number of particles used", fontsize=20)
    plt.ylabel("Problem in the key detection rate ", fontsize=20)
    plt.show()

plotting()
