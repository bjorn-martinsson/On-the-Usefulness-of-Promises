from functools import lru_cache as memoization

"""
    Checks if fiPCSP(A, OR) contains no polymorphisms with matching number >= 4.
    I.e. that fiPCSP(A, OR) has matching number <= 3.
    This is done by going over every function of arity 5 with matching number >= 4,
    and checking if there exists an obstruction.

    Based on Lemma A.2
"""

# f:{0,1}^(t + 1) -> {0, 1}
# f({1}) = f({2}) = ... = f({t}) = 1
def has_atleast_matching_number_t(f: int, t: int) -> bool:
    for i in range(t):
        if (f >> (1 << i)) & 1 == 0:
            return False
    return True

def odd_extension(f: int, L: int) -> int:
    assert f.bit_length() <= 2**L // 2

    for bit in range(2**L // 2):
        bit2 = (~bit) & (2**L - 1) 
        f |= (1 - ((f >> bit) & 1)) << bit2
    return f

@memoization(maxsize=None)
def get_counter_examples(t:int) -> list[int]:
    """
    Find all idempotent functions with matching number t
    and arity t + 1
    """
    out = []
    L = t + 1
    for f in range(0, 2**(2**L//2), 2):
        f2 = odd_extension(f, L)
        if has_atleast_matching_number_t(f2, t):
            out.append(f2)
    return out

def has_matching_number_less_than_t(predicate: list[str], t: int) -> bool:
    k = len(predicate[0])
    # Go over all functions f of arity L = t + 1 with matching number t
    L = t + 1
    for f in get_counter_examples(t):
        # Find all possible obstruction matrices of f

        # Input where f is 0
        zero_inputs = []
        for bit in range(2**L):
            if (f >> bit) & 1 == 0:
                zero_inputs.append(bit)
    
        import itertools
        for mat in itertools.product(zero_inputs, repeat=k):
            # mat is a plausible k x L obstruction matrix
           
            # Check if columns of mat are contained in predicate
            for j in range(L):
                col = ''.join(str((mat[i] >> j) & 1) for i in range(k))
                if col not in predicate:
                    break
            else:
                # Obstruction matrix found of f
                break
        else:
            # No obstruction matrix of f exists
            return False

    # All f have obstruction matrices
    # So predicate must have matching number < t
    return True

MAX_t = 4
def check(predicate: list[str]) -> bool:
    for t in range(3, MAX_t + 1):
        if has_matching_number_less_than_t(predicate, t):
            return True
    return False
