"""
Module that contains tests for the functions in the simulation.
"""
from numpy.random import seed
import pytest
import simulation

@pytest.mark.parametrize("list_lenght", [(1),(100)])
def test_randomly_choose_bases(list_lenght):
    """
    Test the function that randomly choses a base.
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
    """Test on the random initial preparation of the state"""
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
    """
    #Prepare a state
    state = simulation.prepare_particles(n_particles,name)
    #Measure the state
    state_after_measure = simulation.receive_particles(state,name)
    #Test if the state changed, as it should
    assert state_after_measure.all!=state.all

@pytest.mark.parametrize("base_lenght, name", [(1,"Bob"),(100,"Bob")])
def test_compare_bases(base_lenght,name):
    """
    Test for the function that compares two bases. Two different states
    are prepared by 'prepare_particles'. The first state prepared is
    compared with itself, and then with the second state.
    """
    seed(3)
    #Prepare two random states
    state_1 = simulation.prepare_particles(base_lenght,name)
    state_2 = simulation.prepare_particles(base_lenght,name)
    #Compare the same base
    shared_indexes_same = simulation.compare_bases(state_1,state_1)
    #Test that a base compared with itself return same amount of indexes
    assert len(shared_indexes_same) == base_lenght
    #Test that a base compared with itself returns all the indexes
    assert shared_indexes_same == list(range(0,base_lenght))

    shared_indexes_different = simulation.compare_bases(state_1,state_2)
    #Test that when comparing different bases we get different indexes
    assert shared_indexes_different!=shared_indexes_same

@pytest.mark.parametrize(
    "n_particles,detection",
    [(2,True),(9,False),(100,False)]
)
def test_compare_keys_no_eve(n_particles,detection):
    """
    Test for the final function that compares the keys.
    The simulation is run, 'run' returns the result of 'compare_keys'.
    When eavesdropping is False, both 'compare_keys' and 'run' should 
    return False.
    """
    seed(3)
    #Test if with no eavesdropping the simulation detect no interference
    interference = simulation.run(n_particles,eavesdropping=False)
    assert interference == detection
