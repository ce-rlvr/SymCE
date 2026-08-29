import sympy
from sympy import Symbol, oo, Abs, limit

# Top-level setup: define symbols that witness expressions may reference
n = Symbol('n', integer=True, positive=True)

def get_radius(expr):
    """
    Helper function to compute the radius of convergence of a power series
    with coefficients given by `expr` in terms of `n`.
    """
    expr = sympy.sympify(expr)
    if expr == 0:
        return oo
    
    # Try root test first (1 / limsup |a_n|^(1/n))
    try:
        root = limit(Abs(expr)**(1/n), n, oo)
        if root == 0:
            return oo
        elif root == oo:
            return sympy.S(0)
        elif not root.has(oo, sympy.nan, sympy.zoo) and not root.has(n) and not isinstance(root, sympy.Limit):
            return 1 / root
    except Exception:
        pass
    
    # Try ratio test (lim |a_n / a_{n+1}|)
    try:
        ratio = limit(Abs(expr / expr.subs(n, n + 1)), n, oo)
        if not ratio.has(sympy.nan, sympy.zoo) and not ratio.has(n) and not isinstance(ratio, sympy.Limit):
            return ratio
    except Exception:
        pass
        
    return None

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (a_n, b_n, R1, R2), checks if it is a valid counterexample.
    a_n and b_n should be sympy expressions in terms of n.
    R1 and R2 should be the claimed radii of convergence (numbers or sympy.oo).
    """
    try:
        a_n, b_n, R1, R2 = witness
    except Exception:
        return [False, False]
    
    # H_1: a_n has radius of convergence R1
    h1_ok = False
    try:
        R_a = get_radius(a_n)
        if R_a is not None:
            if R_a == R1:
                h1_ok = True
            elif sympy.simplify(R_a - R1) == 0:
                h1_ok = True
    except Exception:
        pass

    # neg_Q: The Hadamard product series a_n * b_n has radius of convergence R < R1 * R2
    neg_q = False
    try:
        R_ab = get_radius(a_n * b_n)
        if R_ab is not None:
            ge_val = (R_ab >= R1 * R2)
            if ge_val == True:
                neg_q = False
            elif ge_val == False:
                neg_q = True
            else:
                neg_q = not bool(ge_val)
    except Exception:
        pass

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: a_n has radius of convergence R1",
    "¬Q: The Hadamard product series has radius of convergence R < R1 * R2"
]

N_HYP = 1
NEG_Q_INDEX = 1