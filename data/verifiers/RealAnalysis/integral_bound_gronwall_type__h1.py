import sympy
from sympy import Symbol, integrate, diff, solve, exp

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
t = Symbol('t', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, C, a, b) or a dictionary with these keys.
    f is a sympy expression in terms of x.
    """
    try:
        if isinstance(witness, dict):
            f_raw = witness['f']
            C = float(witness['C'])
            a = float(witness['a'])
            b = float(witness['b'])
        else:
            f_raw = witness[0]
            C = float(witness[1])
            a = float(witness[2])
            b = float(witness[3])
            
        f = sympy.sympify(f_raw, locals={'x': x, 't': t})
    except Exception:
        return [False, False, False]

    # H_1: C is a non-negative real number
    try:
        h1_ok = bool(C >= 0)
    except Exception:
        h1_ok = False

    # H_2: f(x) <= C + \int_a^x f(t) dt for all x in [a, b]
    try:
        lower = min(a, b)
        upper = max(a, b)
        
        F = integrate(f.subs(x, t), (t, a, x))
        expr = C + F - f
        
        deriv = diff(expr, x)
        try:
            crit_points = solve(deriv, x)
        except Exception:
            crit_points = []
            
        points_to_check = [lower, upper]
        for cp in crit_points:
            try:
                if cp.is_real and lower <= float(cp) <= upper:
                    points_to_check.append(float(cp))
            except Exception:
                pass
                
        # Add sample points across the interval
        for i in range(1, 100):
            points_to_check.append(lower + (upper - lower) * i / 100.0)
            
        h2_ok = True
        for pt in points_to_check:
            val = float(expr.subs(x, pt))
            if val < -1e-7:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # neg_Q: \int_a^b f(x) dx > C * (e^{b-a} - 1)
    try:
        lhs = float(integrate(f, (x, a, b)))
        rhs = C * (float(exp(b - a)) - 1)
        neg_q_ok = bool(lhs > rhs + 1e-7)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: C is a non-negative real number", "H_2: f(x) <= C + integral of f(t) from a to x", "not Q: integral of f(x) from a to b > C * (e^(b-a) - 1)"]

N_HYP = 2
NEG_Q_INDEX = 2