#Diophantine equation:
#6x + 9y + 20z = n is the restriction

#Problem 1
#show that n in [50,51,...,55] is exactly solvable
#with x,y,z being positive integers

import numpy as np

lst_solvable = [50,51,52,53,54,55]
coefs = np.array([6,9,20])

for x in range(10): #x <= 9
    vars = [x,0,0]
    for y in range(7): #y <= 6
        vars[1] = y
        for z in range(3): #z <= 2
            vars[2] = z
            value = coefs.dot(vars)
            if value in lst_solvable:
                lst_solvable.remove(value)
                print(f"vars:{vars}\tvalue:{value}")
            if len(lst_solvable) == 0:
                break
        if len(lst_solvable) == 0:
                break
    if len(lst_solvable) == 0:
                break
print("Done P1\n----------------------")


#Problem 2
'''
Since 50 through 55 are all solvable, every value greater than 55 is also solvable
This is because the smallest increment is 6, and 50-55 are 6 consecutive values. Any value
greater than 55 can be made by taking one of the numbers from 50-55 and adding 6 a certain amount of times.
'''

# #Problem 3
# # Largest non-solvable?
last_unsolvable = 1
current_val = 1 #current value to check
current_streak = 0 #keep track of if theres 6 solvable in a row

def check_val(n, arr_coef):
    for x in range(n // arr_coef[0] + 1):
        vars = [x,0,0]
        for y in range(n // arr_coef[1] + 1):
            vars[1] = y
            if n > 20:
                for z in range(n // arr_coef[2] + 1):
                    vars[2] = z
                    value = arr_coef.dot(vars)
                    if value == n: return True
            else:
                value = arr_coef.dot(vars)
                if value == n: return True

while current_streak < 6: #goes until the minimum required streak of solvables
    if check_val(current_val, coefs): #if it is solvable
        current_streak += 1
    else: #if it isnt solvable
        current_streak = 0
        last_unsolvable = current_val #update the last unsolvable
    current_val += 1 #increment the current value to check

print("largest unsolvable:", last_unsolvable)
print("Done P3\n--------------------")

# Problem 4
# arbitrary coefs array and check up to n = 200 for largest unsolvable
# coefs array is ordered from smallest to largest

def find_largest_unsolvable(coefs: np.ndarray):
    assert len(coefs) == 3
    assert coefs.min() == coefs[0] and coefs.max() == coefs[2]
    assert coefs[1] not in [coefs[0], coefs[2]]
    last_unsolvable = 1
    current_streak = 0
    current_val = 1
    while current_streak < coefs.min() and current_val < 201:
        if check_val(current_val, coefs): #if it is solvable
            current_streak += 1
        else: #if it isnt solvable
            current_streak = 0
            last_unsolvable = current_val #update the last unsolvable
        current_val += 1 #increment the current value to check
    return last_unsolvable

use_coefs = np.array([7,9,30])
p4_answer = find_largest_unsolvable(use_coefs)


print(f'''Given package sizes {use_coefs[0]}, {use_coefs[1]}, and {use_coefs[2]}, the largest number of McNuggets that
cannot be bought in exact quantity is: {p4_answer}''')

#Assign 2 Complete