"""
Module that contains tests for the functions in the simulation.
"""
from numpy.random import seed
import pytest
import simulation

@pytest.mark.parametrize("list_lenght", [(1),(100)])
def test_randomly_choose_bases(list_lenght):
    """
    Test that the function that randomly choses a base works as intended

    Given a reasonable lenght for a base
    When a random base is to be determined
    Then the result is correct, with proper lenght and characters
    """
    base_choices = simulation.randomly_choose_bases(list_lenght)
    #Test that the function doesn't crash and instead returns something
    assert base_choices
    #Test that the lenght of the chosen base is as intended
    assert len(base_choices) == list_lenght
    #Test that the bases cointain only X or Z
    assert (all(flag in ('X','Z') for flag in base_choices))

@pytest.mark.parametrize("n_particles, name", [(1,"Bob"),(100,"Bob")])
def test_preparation(n_particles,name):
    """
    Test that the random initial preparation of the state is valid
    
    Given a reasonable number of particle used, and a name as a string
    When the function is called to prepare a state
    Then the resulting state is the proper lenght
    """
    state = simulation.prepare_particles(n_particles,name)
    #Test if there is an equal number of bases and values
    assert len(state.value)==len(state.base)
    #Test if the lenght of the state values is correct
    assert len(state.value)==n_particles

@pytest.mark.parametrize("n_particles, name", [(1,"Bob"),(100,"Bob")])
def test_receive_particles(n_particles,name):
    """
    Test for the function that emulates a measurement. It's checked that
    a random measurement done a state results in a different state.

    Given a correct state is received
    When a measurement is done on that state
    Then the state should be changed because of the measurement
    """
    #Prepare a state
    state = simulation.prepare_particles(n_particles,name)
    #Measure the state
    state_after_measure = simulation.receive_particles(state,name)
    #Test if the state changed, as it should
    assert state_after_measure.all!=state.all

@pytest.mark.parametrize("base_lenght, name", [(1,"Bob"),(100,"Bob")])
def test_compare_same_bases(base_lenght,name):
    """
    Test for the function that compares two bases. A state is prepared
    by 'prepare_particles' and the it's compared with itself.

    Given a correct state
    When a state is compared with itself
    Then the resulting comparison mathes completely
    """
    seed(3)
    #Prepare a random statee
    state_1 = simulation.prepare_particles(base_lenght,name)
    #Compare the same base
    shared_indexes_same = simulation.compare_bases(state_1,state_1)
    #Test that a base compared with itself return same amount of indexes
    assert len(shared_indexes_same) == base_lenght
    #Test that a base compared with itself returns all the indexes
    assert shared_indexes_same == list(range(0,base_lenght))

@pytest.mark.parametrize("base_lenght, name", [(1,"Bob"),(100,"Bob")])
def test_compare_different_bases(base_lenght,name):
    """
    Test for the function that compares two bases. Two different states
    are prepared by 'prepare_particles'. The first state is then
    compared with the second state, and the result should be different
    than a complete match.

    Given two correct states
    When a state is compared with another
    Then the resulting comparison is not a complete match.
    """
    seed(3)
    #Prepare two random states
    state_1 = simulation.prepare_particles(base_lenght,name)
    state_2 = simulation.prepare_particles(base_lenght,name)
    #Compare the same base
    shared_indexes_same = simulation.compare_bases(state_1,state_1)
    #Compare different bases
    shared_indexes_different = simulation.compare_bases(state_1,state_2)
    #Comparing different bases is different from comparing the same
    assert shared_indexes_different!=shared_indexes_same

@pytest.mark.parametrize(
    "n_particles,detection",
    [(2,True),(9,False),(100,False)]
)
def test_compare_keys_no_eve(n_particles,detection):
    """
    Test for the final function that compares the keys.
    The simulation is run, and the function 'run' returns the result of
    'compare_keys'. When eavesdropping is False 'run' should return
    False, because of no detections. When using few particles instead a
    detection should be found, caused by the impossibility to form a key

    Given a number of particles used in the simulation without Eve
    When the final keys are compared
    Then there should be no detection, unless the number of particles
    used was too low
    """
    seed(3)
    #Test if with no eavesdropping the simulation detect no interference
    interference = simulation.run(n_particles,eavesdropping=False)
    assert interference == detection

@pytest.mark.parametrize(
    "n_particles,detection",
    [(2,True),(9,False),(100,True)]
)
def test_compare_keys_eve(n_particles,detection):
    """
    Test for the final function that compares the keys.
    The simulation is run, and the function 'run' returns the result of
    'compare_keys'. When eavesdropping is Talse 'run' should return
    True, because of ability of the protocol to detect eavesdropping.
    When using a small number of particles, but not too small, the
    chance of detection should be very low, and therefore the result of
    the simulation False.

    Given a number of particles used in the simulation with Eve
    When the final keys are compared
    Then there should a detection, unless the number of particles
    used was low
    """
    seed(3)
    #Test with eavesdropping that the simulation detects it
    interference = simulation.run(n_particles,eavesdropping=True)
    assert interference == detection