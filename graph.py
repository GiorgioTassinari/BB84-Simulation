"""
This module contains functions to launch the BB84 simulation multiple
times to draw a graph plotting the number of particles used and the rate
of detecting a mistake in the key, either caused by a lack of bits to
compare the results or by a detection of an eavesdropper.
The public paramaters 'NUMBER_OF_RUNS' and 'PARTICLE_NUMBER_UPPER_RANGE'
can be used to make the results more accurate and more complete,
respectively. It's noted that increasing these will make the scrit very
slow, so it's suggested to not increse the values too much unless enough
time is available to be spent waiting.
"""
import os
import sys
import matplotlib.pyplot as plt
import simulation

class HiddenPrints:
    """Class to hide the printing done by the simulation runs"""
    def __init__(self):
        self._original_stdout = None
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w',encoding='utf-8')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def simulate_fixed(number_of_runs, particles):
    """
    Runs the simulation a certain number of times, with a fixed number 
    of particles used, and whith eavesdropping turned on. This is to
    find out how many times the eavesdropping is detected. Inability
    during the simulation to compare keys because of low number of bits
    in they is also considered a detection, because it results in a key
    that is unusable for cryptography.

    Parameters
    ----------
        number_of_runs : int
            The number of times the simulation will run
        particles : int
            The number of particles used in each run of the simulation
    Returns
    -------
        failure_rate : float
            The rate of eavesdropping/failures detected by the different
            runs of the simulation over the total number of runs done.
            With high number of particles the failures are caused by the
            dection of an eavesdropper. Failures with very low number of
            particles are caused by the inability to compare the keys.
    """
    number_of_detections = 0
    for _ in range(number_of_runs):
        with HiddenPrints(): #Mute the prints of the simulation
            if simulation.run(n=particles, eavesdropping=True):
                number_of_detections += 1
    failure_rate=number_of_detections/number_of_runs
    return failure_rate

def simulate_multiple(number_of_runs,number_of_particles):
    """
    Run the simulation multiple times, increasing the number of
    particles used in each successive simulation by one each time, up to
    number_of_particles

    Parameters
    ----------
        number_of_runs : int
            The number of times each instance of simulation will run
        number_of_particles : list
            The list containing all the numbers of particles used in
            each successive simulation
    Returns
    -------
        failure_rates: list
            A list containing each failure rate measured by each
            execution of the simulation
    """
    #List to contain all the failing rates calculated by each mutilpe run
    failure_rates = []
    for i,number in enumerate(number_of_particles):
        failure_rates.append(simulate_fixed(number_of_runs,number))
        #Progress counter
        print(f"Executing simulation {i} out of {len(number_of_particles)}",
              end="\r")
    return failure_rates

def plotting(number_of_particles,failure_rates):
    """
    Function that plots the chosen number of paricles on the x axis and
    the detection rate of problems on the y axis.
    Parameters
    ----------
        number_of_particles: list
            The number of particles used in each run of the simulation,
            becomes the x axis
        failure_rates : list
            The failure rate calculated in each run of the simulation,
            becomes the y axis
    Returns
    -------
        None
    """
    plt.figure(figsize=(12,9))
    plt.scatter(number_of_particles, failure_rates, s=40)
    plt.xlabel("Number of particles used", fontsize=20)
    plt.ylabel("Problem in the key detection rate ", fontsize=20)
    plt.show()

def simulate_and_graph(runs=5,particle_max=100):
    """
    Run the simulation how many times as wanted, and then graph it

    Parameters
    ----------
        runs : int, optional
            The number of times each simution is going to run, default 5
        particle_max : int, optional
            Each successive run will increase the number of particles
            sent by 1, starting from 1 and ending with this value,
            default 100
    Returns
    -------
        None
    """
    #List to contain all the failing rates calculated by each mutilpe run
    failure_rates = []
    #List to store the number of particles used in each run of simulation
    number_of_particles = list(range(1,particle_max))
    failure_rates = simulate_multiple(runs,number_of_particles)
    plotting(number_of_particles,failure_rates)

def main():
    """Run the simulations and the graphing"""
    simulate_and_graph()

if __name__ == "__main__":
    main()
