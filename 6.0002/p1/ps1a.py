###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Attar Aziz
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
    dct = {}
    with open(filename, "r") as f:
        for line in f:
            use = line.replace("\n","")
            use = use.split(",")
            dct[use[0]] = int(use[1])
    return dct

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
    cows2 = cows.copy()
    trips = []
    cur_trip = []
    cur_weight = 0
    cur_cow = ""
    while len(cows2.keys()) > 0:
        cur_trip = []
        cur_weight = 0
        while limit - cur_weight >= min(cows2.values()):
            for cow, weight in cows2.items():
                try:
                    if weight > cows2[cur_cow] and weight <= limit - cur_weight:
                        cur_cow = cow
                except KeyError: #if cow was removed or if cur_cow is still ""
                    if weight <= limit - cur_weight: cur_cow = cow
            cur_trip.append(cur_cow)
            cur_weight += cows2[cur_cow]
            del(cows2[cur_cow])
            if len(cows2) == 0: break
        trips.append(cur_trip)
    return trips

# Problem 3
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
    for trips in get_partitions(cows.keys()):
        okay = True
        for trip in trips:
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
                if trip_weight > limit:
                    okay = False
                    break
            if trip_weight > limit:
                break
        if okay:
            try:
                if len(trips) < len(result):
                    result = trips
            except NameError: #the first partition that gets checked
                result = trips
    return result

        
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
    cows = load_cows("ps1_cow_data.txt")
    start = time.perf_counter()
    print(len(greedy_cow_transport(cows)))
    print(time.perf_counter() - start)

    start = time.perf_counter()
    print(len(brute_force_cow_transport(cows)))
    print(time.perf_counter() - start)

if __name__ == "__main__":
    # print("GREEDY:")
    # print(greedy_cow_transport(load_cows("ps1_cow_data.txt")))
    # print("BRUTE FORCE")        
    # print(brute_force_cow_transport(load_cows("ps1_cow_data.txt")))
    
    compare_cow_transport_algorithms()

#Greedy is way faster but does not always get the right answer