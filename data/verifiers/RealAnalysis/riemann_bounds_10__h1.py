import sympy
from sympy import integrate, diff, Symbol

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness can be a dictionary or a tuple containing:
    (a, b, f, phi, [x])
    where a and b are the integration limits, f is the function, phi is the convex function,
    and x is the variable of integration (defaults to the global Symbol 'x').
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            f = witness['f']
            phi = witness['phi']
            v = witness.get('x', x)
        else:
            if len(witness) == 5:
                a, b, f, phi, v = witness
            elif len(witness) == 4:
                a, b, f, phi = witness
                v = x
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if callable(f):
            f_expr = f(v)
        else:
            f_expr = f
            
        if callable(phi):
            phi_expr = phi(v)
        else:
            phi_expr = phi
    except Exception:
        return [False, False, False]

    # H1: a < b
    try:
        h1 = bool(float(a) < float(b))
    except Exception:
        h1 = False

    # H2: phi is a continuous convex function defined on an interval containing the range of f
    try:
        d2 = diff(phi_expr, v, 2)
        pts_to_check = [-10, -1, 0, 1, 10]
        
        # Also check convexity at points in the range of f
        for val in [a, b, (a+b)/2]:
            try:
                f_val = float(f_expr.subs(v, val).evalf())
                pts_to_check.append(f_val)
            except TypeError:
                pass
            
        h2 = True
        for val in pts_to_check:
            eval_d2 = d2.subs(v, val).evalf()
            try:
                # Allow a small floating point tolerance for numerical evaluation
                if float(eval_d2) < -1e-9:
                    h2 = False
                    break
            except TypeError:
                pass
    except Exception:
        h2 = False

    # Conclusion: phi( 1/(b-a) * integrate(f) ) <= 1/(b-a) * integrate(phi(f))
    # We want the conclusion to FAIL, so LHS > RHS
    try:
        int_f = integrate(f_expr, (v, a, b))
        avg_f = int_f / (b - a)
        
        if callable(phi):
            lhs_expr = phi(avg_f)
        else:
            lhs_expr = phi_expr.subs(v, avg_f)
        lhs = lhs_expr.evalf()

        if callable(phi):
            phi_f_expr = phi(f_expr)
        else:
            phi_f_expr = phi_expr.subs(v, f_expr)
            
        int_phi_f = integrate(phi_f_expr, (v, a, b))
        rhs = (int_phi_f / (b - a)).evalf()

        try:
            # Check if LHS > RHS strictly (with a small tolerance to avoid float inaccuracies)
            neg_q = bool(float(lhs) > float(rhs) + 1e-9)
        except TypeError:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a < b",
    "H_2: phi is a continuous convex function defined on an interval containing the range of f",
    "¬Q: phi( 1/(b-a) * int_a^b f(x) dx ) > 1/(b-a) * int_a^b phi(f(x)) dx"
]

N_HYP = 2
NEG_Q_INDEX = 2