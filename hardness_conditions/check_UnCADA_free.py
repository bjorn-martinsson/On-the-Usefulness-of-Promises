from hardness_conditions.unit_propagation import has_obstruction

"""
    Checks if fiPCSP(A, OR) is t-UnCADA-free, for t <= 4.

    Based directly on definition of being t-UnCADA-free, definition 5.19.
"""

def has_cd_obstruction(c: int, d: int, predicate: list[str]) -> bool | None:
    pattern = [d, c, d, 1, 1, 1, 1]

    def UnCADA(x: tuple[int]) -> int | None:
        x,y,z,w1,w2,w3,w4 = x

        # Idempotent + unate
        # f(0,0,0,0,w2,w3,w4) = 0
        idem_property = (x == y == z == w1 == 0)
        if idem_property:
            return 0

        # f(0^d, 0^c, z, w1, 1, w3, w4) = 0
        a_property = (x == y == 0) and (w2 == 1)
        if a_property:
            return 0
        
        # f(x, 0^c, 0^d, w1, w2, 1, w4) = 0
        b_property = (y == z == 0) and (w3 == 1)
        if b_property:
            return 0
        
        # f(x, y, z, 0, w2, w3, 1) = 0 if w(x) + w(y) + w(z) < c + d - 1 
        # and w(w2) + w(w3) >= 1
        c_property = (x + y + z <= c + d - 1) and (w1 == 0) and (w4 == 1) and (w2 + w3 >= 1)
        if c_property:
            return 0
        
        return None

    return has_obstruction(pattern, predicate, UnCADA)

def check_t_UnCADA_free(t: int, predicate: list[str]) -> bool:
    assert t >= 2
    for d in range(1, t):
        c = t - d
        if not has_cd_obstruction(c, d, predicate):
            return False
    return True

MAX_t = 4
def check(predicate: list[str]) -> bool:
    for t in range(2, MAX_t + 1):
        if check_t_UnCADA_free(t, predicate):
            return True
    return False
