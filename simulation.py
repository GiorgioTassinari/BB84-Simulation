"""
This module cointains all the functions to simulate the BB84 protocol
"""
from numpy.random import randint
import pandas as pd

#Class used to add colors to text
class Colors:
    """Class that contains colors used in printing for visual clarity"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'


def randomly_choose_bases(l, name="Someone"):
    """
    When called creates a sequence of random choices of bases (X or Z)
    for the quantum measurement.

    Parameters
    ----------
    l : integer
        Specifies the number of bases that will be chosen
    name : string, optional
        Name used in the message, will descrive who chose the bases
    
    Returns
    -------
    result_string: list
        A string with l lenght of random Xs and Zs
    """
    result_string = []
    for i in range(l):
        if randint(0,2)==0:
            result_string.append("X")
        else:
            result_string.append("Z")
    return result_string

#This this is the measurement done by Alice, who prepares the state
def random_preparation(l, name="Someone"):
    """
    Return a list of random 0 and 1, emulating the results of a series
    of measurements done with random bases on particles in a
    superposition of spin up and down.
    """
    result_list=randint(0,2,l)
    return result_list

def compare_bases(result_1,result_2):
    """
    Compares two sets of bases and visually highlights the values that
    are equal. Save and return them ase these will be the values whose
    results form the key.
    """
    base_1=result_1.base
    base_2=result_2.base
    shared_data = []
    print("The measurements done on the same bases are highlighted in green")
    for i,letter in enumerate(base_1):
        if base_1[i]==base_2[i]:
            #when there is a match, add it to the list
            shared_data.append(result_1.iloc[i].tolist())
            print(f"{Colors.GREEN}"+letter,end="")
        else:
            print(f"{Colors.RED}"+letter,end="")
    print("")
    for i,letter in enumerate(base_2):
        if base_1[i]==base_2[i]:
            print(f"{Colors.GREEN}"+letter,end="")
        else:
            print(f"{Colors.RED}"+letter,end="")
    print(f"{Colors.END}",end="")
    print("")
    print("Now A and B have a shared series of bases with the same results")
    shared_bases=pd.DataFrame(shared_data, columns=['base', 'value'])
    print(shared_bases.transpose())
    return shared_bases

def prepare_particles(n, name):
    """
    Runs all the operations of the first person who prepares the states
    Returns their result as a Dataframe
    """
    #Person chooses random bases
    bases = randomly_choose_bases(n, name)
    #Person measures qubits
    values = random_preparation(n, name)
    result = pd.DataFrame({'base': bases, 'value': values}, columns=['base', 'value'])
    print(name,"chose a random sequence of orthogonal bases and prepared the "
          "states with these values")
    print(result.transpose())
    return result

def receive_particles(n, received_states, name):
    """
    Runs the operations of a person who reeceives a prepared stat
    """
    #Person chooses random bases for measurement
    bases = randomly_choose_bases(n, name)
    #Person measures qubits
    values = []
    for i in range(n):
        if bases[i]==received_states.base[i]:
            values.append(received_states.value[i])
        else: values.append(randint(0,2))
    result = pd.DataFrame({'base': bases, 'value': values}, columns=['base', 'value'])
    print(name,"too chose a random sequence of orthogonal bases and obtained "
          "these results in his measurements")
    print(result.transpose())
    return result

def run(n=10):
    """Run the simulation."""
    alice_result=prepare_particles(n,"Alice")
    bob_result=receive_particles(n, alice_result, "Bob")
    #after enough measurements are done, Alice and Bob share the bases
    compare_bases(alice_result,bob_result)

run()
