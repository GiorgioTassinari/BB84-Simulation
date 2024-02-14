"""
This module cointains all the functions to simulate the BB84 protocol
"""
from numpy.random import randint
import pandas as pd

#To highlight matches in pairs of bases, different colors are useful
class Colors:
    """Class that contains colors used in printing for visual clarity"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m' #Turns coloring of text off, resetting to default

#While doing a measurement in this protocol the bases are chose randomly
def randomly_choose_bases(l):
    """
    Create a sequence of random choices of orthogonal bases (X or Z) for
    the quantum measurement.

    Parameters
    ----------
    l : integer
        Specifies the number of bases that will be chosen

    Returns
    -------
    result_string: list
        A series with lenght l of random Xs and Zs 
    """
    result_string = []
    for _ in range(l):
        if randint(0,2)==0:
            result_string.append("X")
        else:
            result_string.append("Z")
    return result_string

#This this is the measurement done by the sender, who prepares the state
def random_preparation(l):
    """
    Emulates the results of a series of measurements done with random 
    bases on particles in a superposition of spin up and down.

    Parameters
    ----------
    l : integer
        Specifies the number of particles that are measured

    Returns
    -------
    result_list: list
        A series of random 1s and 0s
    """
    result_list=randint(0,2,l)
    return result_list

def prepare_particles(n, name):
    """
    Runs the operations of the first person who prepares the states,
    explaining and printing to terminal the result.

    Parameters
    ----------
    n : integer
        Specifies the number of particles that will be prepared
    name : string, optional
        Name used in printing to describes who chose the bases

    Returns
    -------
    prepared_state: DataFrame
        The result of the preparation of the entangled state
    """
    #Person chooses random bases for preparation
    bases = randomly_choose_bases(n)
    #Person measures qubits
    values = random_preparation(n)
    #Bases chosen and values measured are paired in a dataframe
    prepared_state = pd.DataFrame({'base': bases, 'value': values},
                                  columns=['base', 'value'])
    print(name,"chose a random sequence of orthogonal bases and prepared the "
          "states with these values")
    #transpose shows the result horizontally, making it more readable
    print(prepared_state.transpose())
    return prepared_state

def receive_particles(received_states, name):
    """
    Runs the operations of a person who receives an already prepared 
    state and in doing so, modifies the state. Also explains the result
    and prints it to terminal.

    Parameters
    ----------
    received_states : DataFrame
        The complete state that gets received and measured
    name : string
        Name used in printing to describe who received the state

    Returns
    -------
    prepared_state: DataFrame
        The result of the measurement
    """
    n = len(received_states.index) #number of particles received
    #Person chooses random bases for measurement
    bases = randomly_choose_bases(n)
    values = []
    for i in range(n):
        #when the base chosen by the receiver matches the one chosen
        #by the sender, the result is the same because of entanglement
        if bases[i]==received_states.base[i]:
            values.append(received_states.value[i])
        #if the base chosen is different, the result will be random
        else: values.append(randint(0,2))
    result = pd.DataFrame({'base': bases, 'value': values}, 
                          columns=['base', 'value'])
    print(name,"too chose a random sequence of orthogonal bases and obtained "
          "these results in his measurements")
    print(result.transpose())
    return result

def compare_bases(result_1,result_2):
    """
    Compares two sets of bases and visually highlights the values that
    are equal. Then show these shared bases that have the same results,
    as these results of the measurement will form the shared secret key.

    Parameters
    ----------
    result_1 : DataFrame
        One of the two results to compare with each other
    result_2 : DataFrame
        One of the two results to compare with each other
    
    Returns
    -------
    shared_data_indexes: list
        Contains the indexes of the measurements in which both the 
        sender and the  receiver chose to use the same base for the
        measurement.
    """
    base_1=result_1.base
    base_2=result_2.base
    #shared results, equal if there are no errors or eavesdroppers
    shared_data = []
    #contains the indexes of shared results, to check for errors
    shared_data_indexes = []
    print("The measurements done on the same bases are highlighted in green")
    for i,letter in enumerate(base_1):
        if base_1[i]==base_2[i]:
            #when there is a match it gets added it to the shared lists
            shared_data.append(result_1.iloc[i].tolist())
            shared_data_indexes.append(result_1.index[i])
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
    #create a DataFrame of the results on the shared bases
    shared_bases=pd.DataFrame(shared_data, columns=['bases', 'key'])
    print("Now A and B should have a shared key based on the shared bases")
    print(shared_bases.set_index('bases').transpose())
    return shared_data_indexes

def compare_keys(shared_indexes, sender, receiver):
    """
    Compare the values in the specified indexes

    Parameters
    ----------
        shared_indexes : list
            A list of integers indicating what measurements to compare
        sender : DataFrame
            The complete result of the sender to compare
        receiver : DataFrame
            The complete result of the receiver to compare

    Returns
    -------
        matching_percentage: float
            The percentage of values that matched in the indexes chosen
    """
    sender_values = sender.value
    receiver_values = receiver.value
    #maximum number of result matches when done with the same base
    max_matches=len(shared_indexes)
    #this will incrase by one every time a match is found
    matches = 0
    #index used for the list of indexes
    a = 0
    for i,_ in enumerate(sender_values):
        if i==shared_indexes[a] and sender_values[i] == receiver_values[i]:
            matches += 1
            a += 1
            #to avoid going of bounds in the shared_indexes list
            if matches == max_matches:
                break
    matching_percentage = matches/max_matches*100
    print(f"The matching percentage between the two results is "
          f"{matching_percentage}""%")
    return matching_percentage

def run(n=10, sender="Alice", receiver="Bob"):
    """
    Run the complete simulation.
    
    Parameters
    ----------
        n : int, optional
            How many particles will be used
        sender : string, optional
            The name that will be used in printing for the sender
        receiver : string, optional
            The name that will be used in printing for the receiver
    Returns
    -------
        None
    """
    sender_result=prepare_particles(n,sender)
    receiver_result=receive_particles(sender_result, receiver)
    #after the measurements are done, Alice and Bob share their bases
    shared_bases = compare_bases(sender_result,receiver_result)
    #they also compare a certain number of random bits of the key
    compare_keys(shared_bases, sender_result, receiver_result)

run()
