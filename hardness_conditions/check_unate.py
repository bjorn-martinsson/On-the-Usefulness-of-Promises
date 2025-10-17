from functools import lru_cache as memoization

"""
    Checks if fiPCSP(A, OR) contains no non-unate polymorphisms.
    According to Lemma A.1, this can be done by only studying 
    polymorphisms of arity 5.
"""


# From Lemma A.1.
# f:{0,1}^5 -> {0, 1}
# f(0, 0, 0, 0, 0) = 0
# f(0, 0, 0, 1, 1) = 0
# f(0, 1, 1, 0, 0) = 0
# f(1, 1, 0, 1, 0) = 0
# f(1, 0, 1, 0, 1) = 0
def is_non_unate(f: int) -> bool:
    for x in 0b00000, 0b00011, 0b01100, 0b11010, 0b10101:
        if (f >> x) & 1:
            return False
    return True

def odd_extension(f: int, L: int) -> int:
    assert f.bit_length() <= 2**L // 2

    for bit in range(2**L // 2):
        bit2 = (~bit) & (2**L - 1) 
        f |= (1 - ((f >> bit) & 1)) << bit2
    return f

@memoization(maxsize=None)
def get_counter_examples() -> list[int]:
    """
    Find all idempotent functions that are non-unate according to Lemma A.1
    """
    out = []
    L = 5
    for f in range(0, 2**(2**L//2), 2):
        f2 = odd_extension(f, L)
        if is_non_unate(f2):
            out.append(f2)
    return out

def has_only_unate_polymorphisms(predicate: list[str]) -> bool:
    k = len(predicate[0])
    # Go over functions f of arity L = 5 that are not unate
    L = 5
    for f in get_counter_examples():
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
    # So predicate must only have unate polymorphisms
    return True

def check(predicate: list[str]) -> bool:
    return has_only_unate_polymorphisms(predicate)
