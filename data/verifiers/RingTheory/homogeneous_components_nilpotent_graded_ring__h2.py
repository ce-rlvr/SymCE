import sympy
from sympy import sympify, expand, Poly
from sympy.abc import x, y, z, t, u, v, w

# Top-level setup for potential witness expressions
# The witness is expected to be a tuple: (x, components)
# where x is an element of a commutative graded ring (represented by a sympy expression)
# and components is a list of its homogeneous components.

def is_homogeneous(expr):
    try:
        expr = sympify(expr)
        if expr == 0:
            return True
        expr = expand(expr)
        symbols = list(expr.free_symbols)
        if not symbols:
            return True
        p = Poly(expr, *symbols)
        return p.is_homogeneous
    except Exception:
        return False

def degree_of(expr):
    try:
        expr = sympify(expr)
        if expr == 0:
            return -1
        expr = expand(expr)
        symbols = list(expr.free_symbols)
        if not symbols:
            return 0
        p = Poly(expr, *symbols)
        return p.total_degree()
    except Exception:
        return -1

def is_nilpotent(expr):
    try:
        expr_sym = sympify(expr)
        if expr_sym == 0:
            return True
    except Exception:
        pass

    try:
        if hasattr(expr, 'is_nilpotent'):
            val = expr.is_nilpotent() if callable(expr.is_nilpotent) else expr.is_nilpotent
            if val is True:
                return True
    except Exception:
        pass
    
    return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        x_val, components = witness
        if not isinstance(components, (list, tuple)):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative graded ring
    # We verify that the elements belong to a commutative structure.
    # The graded ring property is implicitly verified by H_2 (polynomials).
    try:
        h1_ok = True
        if not sympify(x_val).is_commutative:
            h1_ok = False
        for xi in components:
            if not sympify(xi).is_commutative:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: x_i are the homogeneous components of x such that x is the sum of x_i
    try:
        x_sym = sympify(x_val)
        comps_sym = [sympify(xi) for xi in components]
        
        h2_ok = True
        if expand(x_sym - sum(comps_sym)) != 0:
            h2_ok = False
        else:
            degrees = []
            for xi in comps_sym:
                if not is_homogeneous(xi):
                    h2_ok = False
                    break
                if xi != 0:
                    d = degree_of(xi)
                    if d in degrees:
                        h2_ok = False
                        break
                    degrees.append(d)
    except Exception:
        h2_ok = False

    # ¬Q: Each homogeneous component x_i is a nilpotent element of R (must FAIL)
    # Negation: At least one homogeneous component x_i is NOT nilpotent.
    try:
        neg_q_ok = False
        for xi in components:
            if not is_nilpotent(xi):
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative graded ring",
    "H_2: x_i are the homogeneous components of x such that x is the sum of x_i",
    "¬Q: At least one homogeneous component x_i is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2