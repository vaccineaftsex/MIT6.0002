###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    data = open(filename, 'r')
    cow_dict = {}
    for line in data:
        (cow_name, cow_weight) = tuple(line.strip().split(","))
        cow_dict[cow_name]= int(cow_weight)
    return cow_dict



# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    sorted_cows = sorted(cows, key = cows.get)
    trip_list = []
    while sorted_cows != []:
        available_weight = limit
        cow_list = []
        while sorted_cows != []:
            new_cow = sorted_cows.pop()
            if available_weight - cows[new_cow] >= 0:
                cow_list.append(new_cow)
                available_weight -= cows[new_cow]
            else:
                sorted_cows.append(new_cow)
                break
        trip_list.append(cow_list)
    return trip_list

#cows = load_cows("ps1_cow_data.txt")
#print(cows)
#print(greedy_cow_transport(cows))


# Problem 3
    
def test_partition(cows, partition, limit):
    """
    Helper function for brute_force_cow_transport. Return whether the allocation given 
    by the partition obeys the weight limitation
    """
    for trip in partition:
        total_weight = 0
        for i in range(len(trip)):
            total_weight += cows[trip[i]]
            if total_weight > limit:
                break
        if total_weight > limit:
            return False
    return True


def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    doable_partition = []
    length_partition = {}   # dict that maps index of partition in doable_partition -> number of trips
    for partition in get_partitions(cows.keys()):
        if test_partition(cows, partition, limit):
            doable_partition.append(partition)
            length_partition[len(doable_partition)] = len(partition)
    return(doable_partition[min(length_partition, key = length_partition.get)])
        
##test1
#cows = {"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}
#print(brute_force_cow_transport(cows))
#
##test 2                
#cows = load_cows("ps1_cow_data.txt")
#print(brute_force_cow_transport(cows))
#




# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows("ps1_cow_data.txt")
    
    print("Greedy algorithm")
    start = time.time()
    best_greedy = greedy_cow_transport(cows)
    end = time.time()
    print("time taken:", end - start, 's')
    print("number of trips:", len(best_greedy),'\n')

    print("Brute-force algorithm")
    start = time.time()
    best_bruteforce = brute_force_cow_transport(cows)
    end = time.time()
    print("time taken:", end - start, 's')
    print("number of trips:", len(best_bruteforce))
    
compare_cow_transport_algorithms()