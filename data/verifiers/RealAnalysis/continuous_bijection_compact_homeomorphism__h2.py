import z3

# Top-level setup
# The witness is expected to use z3 to define the spaces and functions.
# No specific algebraic objects are needed for this Real Analysis theorem.

def to_real(val):
    if isinstance(val, (int, float)):
        return z3.RealVal(val)
    return val

def check_forall(precond, cond):
    solver = z3.Solver()
    solver.set("timeout", 2000)
    solver.add(precond)
    solver.add(z3.Not(cond))
    return solver.check() == z3.unsat

def conditions(witness) -> list[bool]:
    x, x1, x2, x3 = z3.Reals('x x1 x2 x3')
    y, y1, y2, y3 = z3.Reals('y y1 y2 y3')
    eps, delta = z3.Reals('eps delta')
    
    # H1: (X, d_X) and (Y, d_Y) are metric spaces
    try:
        def is_metric(domain, dist, var1, var2, var3):
            s = z3.Solver()
            s.set("timeout", 2000)
            s.add(domain(var1))
            if s.check() != z3.sat: 
                return False
            
            p1 = check_forall(z3.And(domain(var1), domain(var2)), dist(var1, var2) >= 0)
            p2 = check_forall(domain(var1), dist(var1, var1) == 0)
            p3 = check_forall(z3.And(domain(var1), domain(var2), dist(var1, var2) == 0), var1 == var2)
            p4 = check_forall(z3.And(domain(var1), domain(var2)), dist(var1, var2) == dist(var2, var1))
            p5 = check_forall(z3.And(domain(var1), domain(var2), domain(var3)), 
                              dist(var1, var3) <= dist(var1, var2) + dist(var2, var3))
            return p1 and p2 and p3 and p4 and p5

        h1_ok = is_metric(witness.X, witness.d_X, x1, x2, x3) and is_metric(witness.Y, witness.d_Y, y1, y2, y3)
    except Exception:
        h1_ok = False

    # H2: f: X \to Y is a bijective function
    try:
        p1 = check_forall(witness.X(x), witness.Y(witness.f(x)))
        p2 = check_forall(witness.Y(y), witness.X(witness.f_inv(y)))
        p3 = check_forall(witness.X(x), witness.f_inv(witness.f(x)) == x)
        p4 = check_forall(witness.Y(y), witness.f(witness.f_inv(y)) == y)
        h2_ok = p1 and p2 and p3 and p4
    except Exception:
        h2_ok = False

    # H3: f is continuous
    try:
        precond = z3.And(witness.X(x), witness.X(x1), eps > 0)
        delta_val = witness.delta_f(x, eps)
        cond = z3.And(
            delta_val > 0,
            z3.Implies(witness.d_X(x, x1) < delta_val, witness.d_Y(witness.f(x), witness.f(x1)) < eps)
        )
        h3_ok = check_forall(precond, cond)
    except Exception:
        h3_ok = False

    # ¬Q: f^{-1}: Y \to X is not continuous
    try:
        y_star = to_real(witness.y_star)
        eps_star = to_real(witness.eps_star)
        
        s = z3.Solver()
        s.set("timeout", 2000)
        s.add(z3.Not(z3.And(witness.Y(y_star), eps_star > 0)))
        if s.check() != z3.unsat:
            neg_q_ok = False
        else:
            precond = delta > 0
            y_b = witness.y_bad(delta)
            cond = z3.And(
                witness.Y(y_b),
                witness.d_Y(y_star, y_b) < delta,
                witness.d_X(witness.f_inv(y_star), witness.f_inv(y_b)) >= eps_star
            )
            neg_q_ok = check_forall(precond, cond)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: f: X -> Y is a bijective function",
    "H_3: f is continuous",
    "¬Q: f^{-1}: Y -> X is not continuous"
]

N_HYP = 3
NEG_Q_INDEX = 3