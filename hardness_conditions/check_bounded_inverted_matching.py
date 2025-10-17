from hardness_conditions.unit_propagation import has_obstruction

"""
    Checks if fiPCSP(A, OR) contains no polymorphisms with inverted matching number >= 6.
    I.e. that fiPCSP(A, OR) has inverted matching number <= 5.
    This is done by going over every function of arity 9 with inverted matching number >= 6,
    and checking if there exists an obstruction.

    Based on Lemma A.3.
"""

def has_t_obstruction(t: int, predicate: list[str]) -> bool | None:
    pattern = [t+1, 1, 1]

    def f(x: tuple[int]) -> int | None:
        x,a,b = x
        # f(0^(t+1), 0, 0) = 0
        idem_property = (x == a == b == 0)
        if idem_property:
            return 0
        
        # f(1^(t+1), 1, 0) = 0
        a_property = (x == t+1) and (a == 1) and (b == 0)
        if a_property:
            return 0

        # f(x, 0, 1) = 0, |x|=1
        a2_property = (x == 1) and (a == 0) and (b == 1)
        if a2_property:
            return 0
        
        return None

    return has_obstruction(pattern, predicate, f)

def check_t_bounded_inverted_matching(t: int, predicate: list[str]) -> bool:
    assert t >= 1
    if not has_t_obstruction(t, predicate):
        return False
    return True

MAX_t = 6
def check(predicate: list[str]) -> bool:
    for t in range(1, MAX_t + 1):
        if check_t_bounded_inverted_matching(t, predicate):
            return True
    return False
