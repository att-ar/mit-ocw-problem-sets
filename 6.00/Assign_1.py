#1000th prime number
#only check if prime numbers are divisible by prime numbers
#excluding 2 here to save a computation
lst_primes = []
def check_prime(num:int , lst: list) -> list:
    # assert isinstance(num, int), "input is not an integer"
    for i in lst:
        if num % i == 0:
            return None
    lst.append(num)

num_to_check = 3
while len(lst_primes) != 999:
    check_prime(num_to_check, lst_primes)
    num_to_check += 2

print(lst_primes[-1])
#answer should be 7919


#sum of all the ln of the prime numbers from 2 to n:
import numpy as np

def sum_till_n(n):
    new_lst = []
    try:
        for i in range(3,n+1,2):
            check_prime(i, new_lst)
    except TypeError:
        print("did not give an integer")
        return None
    new_lst.append(2)
    return np.sum(np.log(new_lst))

n = 100000
the_sum = sum_till_n(n)
print(the_sum)
print(n)
print(the_sum/float(n))

#Assign 1 completed