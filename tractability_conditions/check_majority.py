"""
Checks if the polymorphisms of fiPCSP(A, OR) contain the majority family.
Based on Lemma 4.3.
"""

def predicate_to_bitmask(predicate: list[str]) -> int:
    out = 0
    for assign in predicate:
        out |= 1 << int(assign, 2)
    return out

def check(predicate: list[str]) -> bool:
    """
    Check if majority is a polymorphism.
    """

    if not predicate:
        return True

    k = len(predicate[0])
    bitmask = predicate_to_bitmask(predicate)
    set_bits = [int(assign, 2) for assign in predicate]
    
    import gurobipy as gp
    from gurobipy import GRB       

    m = gp.Model("my_model_majority")

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
   
    mass = [add_var() for a in set_bits]
    add_constraint(sum(mass) == 1)

    kmass = [0 for i in range(k)]
    for i in range(k):
        for var,a in zip(mass, set_bits):
            if (a >> i) & 1:
                kmass[i] += var

    upper = add_var()
    for var in kmass:
        add_constraint(upper >= var)

    m.setObjective(upper, GRB.MINIMIZE)
    m.optimize()
    
    return get_value(upper) >= 0.5 - 1e-9
