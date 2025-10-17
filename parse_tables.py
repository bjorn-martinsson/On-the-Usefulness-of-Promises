"""
Contains a parser of the files found in ./tables.
See tables/README.md for more information.
"""

def all_bitstrings(k: int) -> list[str]:
    """
        Return all possible bitstring or length k
    """
    out = []
    for i in range(2**k):
        out.append(bin(i + 2**k)[3:])
    return out

def read(FILENAME: str) -> list[list[str]]:
    """
        Read a table file and return all of its predicates
        as a list of lists of strings.
    """
    with open(FILENAME, 'r') as f:
        # Mimic built in input function
        input = lambda: f.readline().rstrip()

        n,k = [int(x) for x in input().split()]  
        predicates = []
        for _ in range(n):
            m = int(input())
            predicate = []
            for S in input().split():
                wildcards = S.count('*')
                # Substitute each wildcard in S by either 0 or 1
                for T in all_bitstrings(wildcards):
                    T = list(T)
                    S_no_wild = [c if c != '*' else T.pop() for c in S]
                    predicate.append(''.join(S_no_wild))
            
            # Sort the predicate (only matters if there were wildcards)
            predicate.sort()
            predicates.append(predicate)
    
    return predicates
