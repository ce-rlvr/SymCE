import sympy as sp

# Top-level setup for potential witness expressions
x, y, z = sp.symbols('x y z', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false Mean Value Theorem for Several Variables.
    The missing hypothesis is that the line segment between a and b must be contained in U.
    
    Witness format: (f, vars, a, b)
    - f: sympy expression for the function
    - vars: tuple of sympy symbols (e.g., (x, y))
    - a: tuple/list of coordinates for point a
    - b: tuple/list of coordinates for point b
    """
    try:
        f, vars, a, b = witness
        a = list(a)
        b = list(b)
    except Exception:
        return [False, False, False]
    
    # H1: a and b are points in R^n
    try:
        h1 = (len(vars) == len(a) == len(b)) and all(sp.sympify(v).is_real for v in a + b)
    except Exception:
        h1 = False

    # H2: f is continuously differentiable on an open set U containing a and b
    # We verify this by checking that f and its gradient are defined and finite at a and b.
    try:
        subs_a = dict(zip(vars, a))
        subs_b = dict(zip(vars, b))
        val_a = f.subs(subs_a)
        val_b = f.subs(subs_b)
        
        if val_a.has(sp.oo, -sp.oo, sp.zoo, sp.nan) or val_b.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
            h2 = False
        else:
            grad_f = [sp.diff(f, v) for v in vars]
            grad_a = [g.subs(subs_a) for g in grad_f]
            grad_b = [g.subs(subs_b) for g in grad_f]
            
            if any(g.has(sp.oo, -sp.oo, sp.zoo, sp.nan) for g in grad_a + grad_b):
                h2 = False
            else:
                h2 = True
    except Exception:
        h2 = False

    # Neg_Q: There is NO point c in the open segment (a, b) such that f(b) - f(a) = ∇f(c) · (b - a)
    try:
        t = sp.Symbol('t', real=True)
        c = [a[i] + t * (b[i] - a[i]) for i in range(len(vars))]
        subs_c = dict(zip(vars, c))
        
        lhs = val_b - val_a
        grad_c = [g.subs(subs_c) for g in grad_f]
        rhs = sum(grad_c[i] * (b[i] - a[i]) for i in range(len(vars)))
        
        diff_expr = lhs - rhs
        
        if sp.simplify(diff_expr) == 0:
            # The equation holds for all t. We just need to check if there is at least one t in (0, 1)
            # where the gradient is defined. We test t = 1/2.
            grad_half = [g.subs(t, sp.Rational(1, 2)) for g in grad_c]
            if not any(g.has(sp.oo, -sp.oo, sp.zoo, sp.nan) for g in grad_half):
                has_valid_c = True
            else:
                has_valid_c = False
        else:
            # Solve for t in the equation diff_expr == 0
            sols = sp.solve(diff_expr, t, dict=True)
            has_valid_c = False
            
            for sol_dict in sols:
                if t in sol_dict:
                    sol = sol_dict[t]
                    try:
                        re, im = sol.evalf().as_real_imag()
                        # Check if the solution is real and strictly between 0 and 1
                        if abs(im) < 1e-9 and 0 < re < 1:
                            grad_c_val = [g.subs(t, sol) for g in grad_c]
                            # Ensure the gradient is actually defined at this point c
                            if not any(g.has(sp.oo, -sp.oo, sp.zoo, sp.nan) for g in grad_c_val):
                                has_valid_c = True
                                break
                    except Exception:
                        pass
        
        neg_q = not has_valid_c
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are points in R^n",
    "H_2: f is continuously differentiable on an open set U containing a and b",
    "¬Q: There is no c in the open segment (a, b) such that f(b) - f(a) = ∇f(c) · (b - a)"
]

N_HYP = 2
NEG_Q_INDEX = 2