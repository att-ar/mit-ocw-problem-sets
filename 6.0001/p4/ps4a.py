# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    #base case
    if len(sequence) == 1: return [sequence]
    
    #recursive step
    else:
        current = get_permutations(sequence[1:])
        new_perms = []
        for perm in current: #perm is a string in new which is a list of permutations
            for i in range(len(perm)):
                new_perms.append(perm[:i] + sequence[0] + perm[i:])
            new_perms.append(perm + sequence[0])
        return new_perms
if __name__ == '__main__':
#    #EXAMPLE
   example_input = 'adc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # pass #delete this line and replace with your code here

