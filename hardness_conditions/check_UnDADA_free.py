from hardness_conditions.unit_propagation import has_obstruction

"""
    Checks if fiPCSP(A, OR) does not contain a t-UnDADA, for t <= 5.

    Based directly on definition of t-UnDADA, definition 5.20.
"""

def has_t_obstruction(t:int, predicate: list[str]) -> bool | None:
    pattern = [1, t-2, 1, 1, 1, 1, 1]

    def UnDADA(x: tuple[int]) -> int | None:
        x1,xmid,xt,y1,y2,y3,z = x

        # Idempotent + unate
        # f(0^t, y, z) = 0
        idem_property = (x1 == xmid == xt == 0)
        if idem_property:
            return 0

        # f(0, 0^(t - 2), xt, 1, 1, y3, z) = 0
        a_property = (x1 == xmid == 0) and (y1 == y2 == 1)
        if a_property:
            return 0
        
        # f(x1, 0^(t - 2), 0, y1, 1, 1, z) = 0
        b_property = (xmid == xt == 0) and (y2 == y3 == 1)
        if b_property:
            return 0
        
        # f(x, y, 1) = 0 if  w(x) <= t - 1 and w(y) >= 2 
        c_property = (x1 + xmid + xt <= t - 1) and (y1 + y2 + y3 >= 2) and (z == 1)
        if c_property:
            return 0
        
        return None

    return has_obstruction(pattern, predicate, UnDADA)

def check_t_UnDADA_free(t: int, predicate: list[str]) -> bool:
    assert t >= 3
    if not has_t_obstruction(t, predicate):
        return False
    return True

MAX_t = 5
def check(predicate: list[str]) -> bool:
    for t in range(3, MAX_t + 1):
        if check_t_UnDADA_free(t, predicate):
            return True
    return False
