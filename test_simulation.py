"""
Module that contains tests for the functions in the simulation.
Some of the strategies used in the tests only considers ints between a 
limited range with less max examples and higher deadline than default 
because the test freezes or reports unwanted timeout failures otherwise.
"""
import datetime
from hypothesis import settings, given, strategies as st
import simulation

@given(st.integers(-1000,1000))
@settings(max_examples = 50, deadline=datetime.timedelta(milliseconds=300))
def test_randomly_choose_bases(l):
    """
    Test the function that randomly choses a base.
    """
    base_choices = simulation.randomly_choose_bases(l)
    #Test that the function doesn't crash and instead returns something
    assert base_choices is not None
    if l>0:
        #Test that the lenght of the chosen base is as intended
        assert len(base_choices) == l
        #Test that the bases cointain only X or Z
        assert (all(flag in ('X','Z') for flag in base_choices))

@given(st.integers(-10000,10000),st.text())
def test_preparation(n,name):
    """Test on the random initial preparation of the state"""
    state = simulation.prepare_particles(n,name)
    #Test if there is an equal number of bases and values
    assert len(state.value)==len(state.base)
    if n>0:
        #Test if the lenght of the state values is correct
        assert len(state.value)==n

@given(st.integers(-1000,1000),st.text())
def test_receive_particles(n,name):
    """Test for the function that emulates a measurement"""
    #Prepare a state
    state = simulation.prepare_particles(n,name)
    #Measure the state
    state_after_measure = simulation.receive_particles(state,name)
    #Test if the state changed, as it should
    assert state_after_measure is not state
