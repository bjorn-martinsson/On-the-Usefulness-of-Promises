"""
Checks if the polymorphisms of fiPCSP(A, OR) contain the parity family.
Based on Lemma 4.4.
"""

def check(predicate: list[str]) -> bool:
    """
    Check if odd parity is a polymorphism.
    """

    if not predicate:
        return True

    k = len(predicate[0])
    set_bits = [int(assign, 2) for assign in predicate]
    
    A = [a + 2**k for a in set_bits]
    B = []
    # Gaussian elemination algorithm implemented via integer operations
    for a in A:
        for b in B:
            a = min(a, a ^ b)
        if a:
            B.append(a)

    a = 2**k
    for b in B:
        a = min(a, a ^ b)
    return a > 0
