from hardness_conditions.unit_propagation import has_obstruction

"""
    Checks if fiPCSP(A, OR) is t-ADA-free, for t <= 5.

    Based directly on definition of ADA, definition 5.11.
"""

def has_cd_obstruction(c: int, d: int, predicate: list[str]) -> bool | None:
    pattern = [1, d, c, d]

    def ADA(x: tuple[int]) -> int | None:
        a,x,y,z = x
        # f(0, 0^d, 0^c, 0^d) = 0
        idem_property = (a == x == y == z == 0)
        if idem_property:
            return 0

        # f(1, 1^d, 0^c, 0^d) = 0
        a_property = (a == 1) and (x == d) and (y == 0) and (z == 0)
        if a_property:
            return 0
        
        # f(1, 0^d, 0^c, 1^d) = 0
        a2_property = (a == 1) and (x == 0) and (y == 0) and (z == d)
        if a2_property:
            return 0

        # f(0, x, y, z) = 0 if at most one of (x=1^d) (y=1^c) (ẑ=1^d) are true
        b_property = (a == 0) and ((x == d) + (y == c) + (z == d) <= 1)
        if b_property:
            return 0

        # f(0, x, y, z) = 0 if w(x) + w(y) + w(z) < c + d
        c_property = (a == 0) and (x + y + z < c + d)
        if c_property:
            return 0
        
        return None

    return has_obstruction(pattern, predicate, ADA)

def check_t_ADA_free(t: int, predicate: list[str]) -> bool:
    assert t >= 2
    for d in range(1, t):
        if not has_cd_obstruction(t - d, d, predicate):
            return False
    return True

MAX_t = 5
def check(predicate: list[str]) -> bool:
    for t in range(2, MAX_t + 1):
        if check_t_ADA_free(t, predicate):
            return True
    return False
