"""
Checks if the polymorphisms of fiPCSP(A, OR) contain the idempotized minorty family.
Based on Lemma 4.6.
"""

def check(predicate: list[str]) -> bool:
    """
    Check if idempotized minority is a polymorphism.
    """
    if not predicate:
        return True

    k = len(predicate[0])
    set_bits = [int(assign, 2) for assign in predicate]
    
    for mask0 in range(2**k):
        # 0 bits in mask forces coordinates to be 0

        A = [a for a in set_bits if a & mask0 == a]
        
        if not A:
            continue

        fixed = mask0
        for a in A:
            fixed &= a

        if fixed:
            continue
       
        import gurobipy as gp
        from gurobipy import GRB       

        m = gp.Model("my_model_miniority")

        m.Params.NumericFocus = 3
        m.Params.FeasibilityTol = 1e-9
        m.Params.IntFeasTol = 1e-9
        m.Params.OptimalityTol = 1e-9
        m.Params.MIPGap = 1e-17
        
        def add_var(ub = 1):
            return m.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = ub)

        def add_constraint(test):
            m.addConstr(test)

        def get_value(x):
            if isinstance(x, int) or isinstance(x, float):
                return x
            if isinstance(x, gp.LinExpr):
                return x.getValue()
            return x.X
       
        mass = [add_var() for a in A]
        add_constraint(sum(mass) == 1)

        kmass = [0 for i in range(k)]
        for i in range(k):
            for var,a in zip(mass, A):
                if (a >> i) & 1:
                    kmass[i] += var

        lower = add_var()
        for i in range(k):
            if (mask0 >> i) & 1:
                add_constraint(lower <= kmass[i])

        m.setObjective(lower, GRB.MAXIMIZE)
        m.optimize()
        
        if get_value(lower) > 0.5 + 1e-9:
            return False
    return True
