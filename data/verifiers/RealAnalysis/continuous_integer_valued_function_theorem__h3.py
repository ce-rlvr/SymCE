import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The conjecture is: If f is continuous on the interval, then f is constant.
    (The dropped hypothesis was that f takes only integer values).
    """
    try:
        # Witness can be a tuple (f, a, b) or just an expression f (defaulting to 0 to 1)
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            f, a, b = witness
        else:
            f = witness
            a = sympy.Integer(0)
            b = sympy.Integer(1)
            
        if not isinstance(f, sympy.Expr):
            f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]

    var = x
    try:
        free_symbols = f.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) > 1:
            return [False, False, False]
    except Exception:
        pass

    # H_1: f is a real-valued function defined on the closed interval
    h1 = False
    try:
        if a.is_real and b.is_real and bool(a < b):
            v1 = f.subs(var, a).evalf()
            v2 = f.subs(var, b).evalf()
            v3 = f.subs(var, a + (b - a) / 2).evalf()
            
            if v1.is_real and v2.is_real and v3.is_real:
                h1 = True
    except Exception:
        h1 = False

    # H_2: f is continuous at every point in the interval
    h2 = False
    try:
        from sympy.calculus.util import continuous_domain
        domain = continuous_domain(f, var, sympy.Interval(a, b))
        h2 = (domain == sympy.Interval(a, b))
    except Exception:
        try:
            # Fallback if continuous_domain fails
            h2 = bool(f.is_polynomial(var))
        except Exception:
            h2 = False

    # ¬Q: The function f is not constant on the interval
    neg_q = False
    try:
        exact_a = sympy.simplify(f.subs(var, a))
        exact_b = sympy.simplify(f.subs(var, b))
        exact_mid = sympy.simplify(f.subs(var, a + (b - a) / 2))
        
        if exact_a == exact_b == exact_mid:
            neg_q = False
        else:
            val_a = f.subs(var, a).evalf()
            val_b = f.subs(var, b).evalf()
            val_mid = f.subs(var, a + (b - a) / 2).evalf()
            
            diff1 = sympy.Abs(val_a - val_b).evalf()
            diff2 = sympy.Abs(val_a - val_mid).evalf()
            
            if diff1.is_number and diff2.is_number:
                if bool(diff1 < 1e-9) and bool(diff2 < 1e-9):
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval",
    "H_2: f is continuous at every point in the interval",
    "¬Q: The function f is not constant on the interval"
]

N_HYP = 2
NEG_Q_INDEX = 2