###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    try:
        return memo[target_weight]
    except KeyError:
        if target_weight == 0:
            return 0
        elif target_weight < 0:
            return float("inf") #so that any number of eggs will be less than this
            #avoids being caught in a loop of zeros
        
        #MY NOTE:
        #want to break the problem into a smaller one: target_weight = target_weight - weight of egg
        #so you pass the new target weight with the list of egg_weights available
        #ex) from 99, use (1,5,10,25), 99 - one of [1,5,10,25], memo
        #   becomes target_weight, use (1,5,10,25), target_weight - one of [1,5,10,25], memo, etc
        # the algorithm will go through egg_weights in each recursion and in the end will give the smallest num
        cur_count = float("inf")
        for egg in egg_weights:
            cur_eggs = dp_make_weight(egg_weights, target_weight - egg, memo)
            cur_eggs += 1 #add the egg that was actually used
            if cur_eggs < cur_count:
                cur_count = cur_eggs
        
        memo[target_weight] = cur_count
        return cur_count
        #I need to learn how to conceptualize what the smaller problem is
        #objective function: num eggs that add up to the target weight
        # want to minimize
        #constraint: target_weight
        #smaler problem: num eggs that add up to target_weight - weight of one weight in `egg_weights` being considered
        #base case: target_weight == 0: return 0 #cant have any eggs here
        # second base case: target_weight < 0: return infinity since this cannot be the solution
        #  the infinity ensures that any valid value of number of eggs computed is taken because it will be less than infinity

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()