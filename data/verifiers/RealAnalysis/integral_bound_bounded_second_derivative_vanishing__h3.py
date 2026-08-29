import sympy as sp

# Top-level setup
x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, dict):
            f_expr = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            M = witness.get('M')
        elif hasattr(witness, 'f') and hasattr(witness, 'a') and hasattr(witness, 'b') and hasattr(witness, 'M'):
            f_expr = witness.f
            a = witness.a
            b = witness.b
            M = witness.M
        else:
            f_expr, a, b, M = witness
    except Exception:
        return [False, False, False]

    try:
        a_val = sp.sympify(a)
        b_val = sp.sympify(b)
        f_expr = sp.sympify(f_expr)
        M_val = sp.sympify(M)
        
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) > 1:
            var = x if x in free_syms else list(free_syms)[0]
        else:
            var = x
    except Exception:
        return [False, False, False]

    # H1: f is a twice continuously differentiable real-valued function on the interval from a to b
    try:
        if a_val.is_number and b_val.is_number:
            a_f = a_val.evalf()
            b_f = b_val.evalf()
            if sp.im(a_f) == 0 and sp.im(b_f) == 0 and bool(a_f < b_f):
                f_prime = sp.diff(f_expr, var)
                f_double_prime = sp.diff(f_prime, var)
                h1 = isinstance(f_double_prime, sp.Expr)
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: f(a) = 0 and f(b) = 0
    try:
        val_a = f_expr.subs(var, a_val)
        val_b = f_expr.subs(var, b_val)
        if val_a.is_number and val_b.is_number:
            h2 = (abs(val_a.evalf()) < 1e-12) and (abs(val_b.evalf()) < 1e-12)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: |\int_a^b f(x) dx| > M(b-a)^3 / 12
    try:
        integral_val = sp.integrate(f_expr, (var, a_val, b_val))
        lhs = abs(integral_val)
        rhs = M_val * (b_val - a_val)**3 / 12
        diff = lhs - rhs
        if diff.is_number:
            neg_q = bool(diff.evalf() > 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a twice continuously differentiable real-valued function on the interval from a to b",
    "H_2: f(a) = 0 and f(b) = 0",
    "not Q: |int_a^b f(x) dx| > M(b-a)^3 / 12"
]

N_HYP = 2
NEG_Q_INDEX = 2