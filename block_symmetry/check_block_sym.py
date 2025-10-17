"""
This file contain tests for if fiPCSP(A, OR) have symmetric/block-symmetric polymorphisms.
This is done using the SAT-solver Glucose3 found in pysat.

This file provides both check_sym (symetric polymorphisms of odd arity L <= 31) 
and check_block_sym (block-symmetric polymorphisms of arity L x (L + 1), where L <= 11).
For the verification, it is only relevant to consider the block-symmetric case.
"""

def minkowski(A: set[tuple], B: set[tuple]) -> set[tuple]:
    """
    Compute the Minkowski sum of A and B
    """
    C = set()
    for a in A:
        for b in B:
            c = tuple(aa+bb for aa,bb in zip(a, b))
            C.add(c)
    return C

CHECK_SYM_UP_TO = 31
def check_sym(predicate: list[str]) -> tuple[int, list[int]]:
    """
    Check if predicate has symmetric polymorpisms of all odd arities <= CHECK_SYM_UP_TO.

    If an odd arity L <= CHECK_SYM_UP_TO is found where no symmmetric polymorphism exists,
    then (L, []) is returned.

    Otherwise (CHECK_SYM_UP_TO, truth_table) is returned, where truth_table is a truth table
    of a symmetric polymorphism of arity CHECK_SYM_UP_TO.
    """
    
    # We do not allow predicate to be empty
    assert predicate

    k = len(predicate[0])
    satis = [tuple(int(x) for x in assign) for assign in predicate]
    
    reachable = set(satis)
    L = 1
    while L < CHECK_SYM_UP_TO:
        L += 2
        reachable = minkowski(reachable, satis)
        reachable = minkowski(reachable, satis)

        SAT = {tuple(sorted(set(c))) for c in reachable}
        num_var = (L + 1) // 2
            
        # Create and solve SAT instance for polymorphism
        from pysat.solvers import Glucose3
        g = Glucose3()
        g.add_clause([-1])

        for clause in SAT:
            g.add_clause([x + 1 if x < num_var else x-L-1 for x in clause])

        if g.solve():
            # Solution found!
            assignment = g.get_model()
            assignment = [+(a>0) for a in assignment]
            assignment += [0] * (num_var - len(assignment))
            for i in range(num_var):
                assignment[~i] = 1 - assignment[i]
        else:
            # No L arity symetric polymorphism exists
            return L, []

    # Symetric polymorhpism exists for all odd arities <= CHECK_SYM_UP_TO
    # Return 31-arity symetric polymorhpism
    return L, assignment

CHECK_BLOCK_SYM_UP_TO = 11
def check_block_sym(predicate: list[str]) -> tuple[int, list[int]]:
    """
    Check if predicate has L x (L+1) block symmetric polymorpisms, for all L <= CHECK_BLOCK_SYM_UP_TO.

    If an odd L <= CHECK_BLOCK_SYM_UP_TO is found where no L x (L + 1) block symmmetric polymorphism exists,
    then (L, []) is returned.

    Otherwise (CHECK_BLOCK_SYM_UP_TO, truth_table) is returned, where truth_table is a truth table
    of a L x (L + 1) block symmetric polymorphism, with L = CHECK_BLOCK_SYM_UP_TO.
    """

    # We do not allow predicate to be empty
    assert predicate

    k = len(predicate[0])
    satis = [tuple(int(x) for x in assign) for assign in predicate]

    reachable_large = set(satis)
    L = 0
    while L < CHECK_BLOCK_SYM_UP_TO:
        L += 1
        # Look for existence of any L x (L + 1) block sym polymorphism
        reachable_small = reachable_large
        reachable_large = minkowski(reachable_small, satis)

        SAT = set()
        for c_small in reachable_small:
            for c_large in reachable_large:
                c = {a + b * (L+1) for a,b in zip(c_small, c_large)}
                SAT.add(tuple(sorted(c)))

        # number of variables needed is (maxval + 1)//2
        # where maxval is L + (L + 1)**2
        maxval = L + (L + 1)**2
        num_var = (maxval + 1)//2

        from pysat.solvers import Glucose3
        g = Glucose3()
        
        for clause in SAT:
            # Currently f(c) = f(a, b) where a,b = moddiv(c, L + 1)
            # To make f odd, we require f(c) = 1-f(maxval - c)
            
            # To avoid creating double the number of neccessary variables
            # Use the negation of c if c >= num_var
            # Negation of c is ~c (bit inverse) when 0 indexing
            def get_variable_0index(c: int) -> int:
                if c < num_var:
                    return c
                else:
                    return ~(maxval - c)

            # SAT solver uses strictly positive indices for a variable, and - that for its inverse
            # I.e. 1-indexing
            def get_variable_1index(c: int) -> int:
                x = get_variable_0index(c)
                if x >= 0:
                    return x + 1
                else:
                    return x
             
            g.add_clause([get_variable_1index(x) for x in clause])
        
        # Require f(0) = 0
        g.add_clause([-1])

        if g.solve():
            # Solution found! I.e. block symmetric polymorphism found
            assignment = g.get_model()
            assignment = [+(a>0) for a in assignment]
            assignment += [0] * (num_var - len(assignment))
            for i in range(num_var):
                assignment[~i] = 1 - assignment[i]
        else:
            # No block symmetric polymorphism exists
            return L, []

    # Block symetric polymorhpism exists for all L x (L + 1), L <= CHECK_BLOCK_SYM_UP_TO
    return L, assignment
