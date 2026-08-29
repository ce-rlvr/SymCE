import sympy
from sympy import Symbol

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def check_bounded(expr, var):
    """
    Heuristically checks if a sympy expression is bounded on the real line.
    """
    try:
        expr = sympy.sympify(expr)
    except Exception:
        return False

    if expr.is_constant():
        try:
            v = complex(expr)
            if abs(v.imag) > 1e-7:
                return False
            return True
        except Exception:
            return False

    # Check for poles by finding real roots of the denominator
    try:
        num, den = expr.as_numer_denom()
        if den != 1 and den.is_polynomial(var):
            roots = sympy.real_roots(den)
            for r in roots:
                lim = sympy.limit(expr, var, r)
                if lim == sympy.oo or lim == -sympy.oo or lim == sympy.zoo or lim.has(sympy.oo, -sympy.oo, sympy.zoo):
                    return False
    except Exception:
        pass

    # Check limits at infinity
    try:
        L1 = sympy.limit(expr, var, sympy.oo)
        if L1 == sympy.oo or L1 == -sympy.oo or L1 == sympy.zoo or L1.has(sympy.oo, -sympy.oo, sympy.zoo):
            return False
        L2 = sympy.limit(expr, var, -sympy.oo)
        if L2 == sympy.oo or L2 == -sympy.oo or L2 == sympy.zoo or L2.has(sympy.oo, -sympy.oo, sympy.zoo):
            return False
    except Exception:
        pass

    # Check values at a wide range of test points
    try:
        test_points = [
            0, 1, -1, 2, -2, 5, -5,
            10, -10, 100, -100, 1000, -1000, 
            10000, -10000, 100000, -100000, 1000000, -1000000,
            2000000, -2000000, 5000000, -5000000,
            10000000, -10000000,
            1e10, -1e10, 1e15, -1e15, 1e20, -1e20,
            1e-2, -1e-2, 1e-4, -1e-4, 1e-6, -1e-6,
            3.1415926535, 1.5707963267, 2.718281828
        ]
        for val in test_points:
            try:
                evaluated = expr.subs(var, val).evalf()
                if evaluated.has(sympy.oo, -sympy.oo, sympy.zoo):
                    return False
                if evaluated.has(sympy.nan):
                    continue
                v = complex(evaluated)
                if abs(v.imag) > 1e-7:
                    return False
                if abs(v.real) > 1e7:
                    return False
            except OverflowError:
                return False
            except Exception:
                continue
        return True
    except Exception:
        return False

def check_lipschitz(expr, var):
    """
    Heuristically checks if a sympy expression is Lipschitz continuous on the real line
    by checking if its derivative is bounded.
    """
    try:
        expr = sympy.sympify(expr)
        if expr.is_constant():
            return True
        dexpr = sympy.diff(expr, var)
        return check_bounded(dexpr, var)
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness tuple (f_expr, g_expr), checks if it satisfies the hypotheses
    and violates the conclusion of the conjecture.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        f_expr, g_expr = witness
    except Exception:
        return [False, False, False]
    
    # H_1: f is bounded and Lipschitz continuous
    try:
        h1_ok = bool(check_bounded(f_expr, x) and check_lipschitz(f_expr, x))
    except Exception:
        h1_ok = False
        
    # H_2: g is bounded and Lipschitz continuous
    try:
        h2_ok = bool(check_bounded(g_expr, x) and check_lipschitz(g_expr, x))
    except Exception:
        h2_ok = False
        
    # ¬Q: The quotient function f/g is NOT Lipschitz continuous on R
    try:
        quotient = f_expr / g_expr
        neg_q_ok = not bool(check_lipschitz(quotient, x))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is bounded and Lipschitz continuous on R",
    "H_2: g is bounded and Lipschitz continuous on R",
    "¬Q: The quotient function f/g is not Lipschitz continuous on R"
]

N_HYP = 2
NEG_Q_INDEX = 2