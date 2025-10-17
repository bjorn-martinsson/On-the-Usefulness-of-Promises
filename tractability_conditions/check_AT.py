"""
Checks if the polymorphisms of fiPCSP(A, OR) contain the AT family.
Based on Lemma 4.5.
"""

def check(predicate: list[str]) -> bool:
    """
    Check if AT is a polymorphism.
    """

    if not predicate:
        return True

    k = len(predicate[0])
    set_bits = [int(assign, 2) for assign in predicate]

    import gurobipy as gp
    from gurobipy import GRB       

    m = gp.Model("my_model_AT")

    m.Params.NumericFocus = 3
    m.Params.FeasibilityTol = 1e-9
    m.Params.IntFeasTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    m.Params.MIPGap = 1e-17
    
    def add_var(lb = -1, ub = 1):
        return m.addVar(vtype=GRB.CONTINUOUS, lb = lb, ub = ub)

    def add_constraint(test):
        m.addConstr(test)

    def get_value(x):
        if isinstance(x, int) or isinstance(x, float):
            return x
        if isinstance(x, gp.LinExpr):
            return x.getValue()
        return x.X
  
    
    kmass = [add_var(0, 1) for _ in range(k)]
    add_constraint(sum(kmass) == 1)
    
    goal = add_var(-1, 1)

    mass = [0 for a in set_bits]

    for i in range(k):
        for j,a in enumerate(set_bits):
            if (a >> i) & 1:
                mass[j] -= kmass[i]
            else:
                mass[j] += kmass[i]

    for var in mass:
        add_constraint(var == goal)
    
    m.setObjective(goal, GRB.MINIMIZE)
    m.optimize()
    
    if m.Status == GRB.INFEASIBLE:
        return False

    return get_value(goal) < 1.0
