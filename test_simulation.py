"""
Module that contains tests
"""
import datetime
from hypothesis import settings, given, strategies as st
import simulation

@given(st.integers(-10000,10000))
@settings(max_examples = 50, deadline=datetime.timedelta(milliseconds=300))
def test_randomly_choose_bases(l):
    """testing that the function returns something"""
    base_choices = simulation.randomly_choose_bases(l)
    assert base_choices is not None

@given(st.integers(0,10000))
@settings(max_examples = 50, deadline=datetime.timedelta(milliseconds=300))
def test_randomly_choose_bases_positive(l):
    """testing the lenght of the chosen base is as intended"""
    base_choices = simulation.randomly_choose_bases(l)
    assert len(base_choices) == l
