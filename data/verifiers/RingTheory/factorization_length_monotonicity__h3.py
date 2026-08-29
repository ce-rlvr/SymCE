import sympy
import sympy.ntheory
import sympy.polys

x, y, z, t = sympy.symbols('x y z t')

def L(val):
    if isinstance(val, (int, sympy.Integer)):
        if val == 0: 
            return 0
        if abs(val) == 1: 
            return 0
        factors = sympy.ntheory.factorint(abs(val))
        return sum(factors.values())
    elif isinstance(val, sympy.Expr):
        factors = sympy.factor_list(val)
        return sum(mult for factor, mult in factors[1])
    return 0

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        is_int_a = isinstance(a, (int, sympy.Integer))
        is_int_b = isinstance(b, (int, sympy.Integer))
        is_poly_a = isinstance(a, sympy.Expr) and not is_int_a
        is_poly_b = isinstance(b, sympy.Expr) and not is_int_b
        
        h1 = bool((is_int_a or is_poly_a) and (is_int_b or is_poly_b))
    except Exception:
        h1 = False

    try:
        if is_int_a:
            h2 = bool(a != 0 and abs(a) != 1)
        elif is_poly_a:
            h2 = bool(a != 0 and not a.is_number)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if is_int_b:
            h3 = bool(b != 0 and abs(b) != 1)
        elif is_poly_b:
            h3 = bool(b != 0 and not b.is_number)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        neg_q = bool(L(a) <= L(b))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: a and b are elements of a UFD", "H_2: a is non-zero and non-unit", "H_3: b is non-zero and non-unit", "¬Q: L(a) <= L(b)"]
N_HYP = 3
NEG_Q_INDEX = 3