"""
Checks if the polymorphisms of fiPCSP(A, OR) contain the idempotized even parity family.
Based on Lemma 4.7.
"""

def check(predicate: list[str]) -> bool:
    """
    Check if idempotized even parity is a polymorphism.
    """
    if not predicate:
        return True

    k = len(predicate[0])
    set_bits = [int(assign, 2) for assign in predicate]

    for mask0 in range(2**k):
        # 0 bits in mask0 forces coordinates to be 0
       
        A = [a for a in set_bits if a & mask0 == a]
        
        if not A:
            continue

        fixed = mask0
        for a in A:
            fixed &= a

        if fixed:
            continue
        
        Ak = [a + 2**k for a in A]

        B = []
        # Gaussian elemination implented via integer operations
        for a in Ak:
            for b in B:
                a = min(a, a ^ b)
            if a:
                B.append(a)

        a = 2**k + mask0
        for b in B:
            a = min(a, a ^ b)

        if a == 0:
            return False
    return True
