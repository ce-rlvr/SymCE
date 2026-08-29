import sympy as sp
import math

z = sp.Symbol('z', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide a function f, a point x, and a step h.
    """
    if isinstance(witness, dict):
        f_expr = witness.get('f', z)
        x_val = witness.get('x', 0)
        h_val = witness.get('h', 0)
        var = witness.get('var', z)
    elif isinstance(witness, (list, tuple)):
        if len(witness) >= 3:
            f_expr = witness[0]
            x_val = witness[1]
            h_val = witness[2]
        else:
            return [False, False]
        var = z
        if hasattr(f_expr, 'free_symbols') and len(f_expr.free_symbols) == 1:
            var = list(f_expr.free_symbols)[0]
    else:
        return [False, False]

    try:
        f3 = sp.diff(f_expr, var, 3)
        v1 = f3.subs(var, x_val - h_val)
        v2 = f3.subs(var, x_val)
        v3 = f3.subs(var, x_val + h_val)
        
        def is_valid(v):
            try:
                v_f = complex(sp.N(v))
                if math.isinf(v_f.real) or math.isnan(v_f.real):
                    return False
                return abs(v_f.imag) < 1e-9
            except Exception:
                return False
                
        H1 = is_valid(v1) and is_valid(v2) and is_valid(v3)
    except Exception:
        H1 = False

    try:
        h_float = float(sp.N(h_val))
        if h_float <= 0.0:
            neg_Q = True
        else:
            f1 = sp.diff(f_expr, var, 1)
            
            LHS = (f_expr.subs(var, x_val + h_val) - f_expr.subs(var, x_val - h_val)) / (2 * h_val) - f1.subs(var, x_val)
            LHS = sp.simplify(LHS)
            
            c = sp.Symbol('c', real=True)
            RHS = (h_val**2 / 6) * f3.subs(var, c)
            
            eq = sp.simplify(LHS - RHS)
            if eq == 0:
                neg_Q = False
            else:
                sols = sp.solve(eq, c)
                
                lower = float(sp.N(x_val - h_val))
                upper = float(sp.N(x_val + h_val))
                if lower > upper:
                    lower, upper = upper, lower
                    
                found = False
                for sol in sols:
                    try:
                        sol_c = complex(sp.N(sol))
                        if abs(sol_c.imag) < 1e-9:
                            if lower < sol_c.real < upper:
                                found = True
                                break
                    except Exception:
                        pass
                neg_Q = not found
    except Exception:
        neg_Q = False

    return [bool(H1), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: f is three times continuously differentiable on the interval",
    "¬Q: There does not exist c in the interval such that the equation holds"
]

N_HYP = 1
NEG_Q_INDEX = 1