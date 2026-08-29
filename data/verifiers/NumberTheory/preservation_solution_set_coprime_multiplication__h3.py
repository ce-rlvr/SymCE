import math
import sympy
from sympy import Rational, Integer

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: a, b, c, m are integers with m > 0",
    "H_2: \\gcd(c, m) = 1",
    "¬Q: x is a solution to exactly one of ax \\equiv b \\pmod m and acx \\equiv bc \\pmod m"
]

def is_integer_val(v):
    if isinstance(v, int):
        return True
    if isinstance(v, float):
        return v.is_integer()
    try:
        v_sym = sympy.sympify(v)
        if v_sym.is_integer is True:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            m = witness['m']
            x = witness['x']
        else:
            a, b, c, m, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: a, b, c, m are integers with m > 0
    try:
        h1 = (is_integer_val(a) and is_integer_val(b) and 
              is_integer_val(c) and is_integer_val(m) and bool(m > 0))
    except Exception:
        h1 = False

    # H_2: \gcd(c, m) = 1
    try:
        if is_integer_val(c) and is_integer_val(m):
            h2 = math.gcd(int(c), int(m)) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: x is a solution to exactly one of the congruences
    try:
        sym_a = sympy.sympify(a)
        sym_b = sympy.sympify(b)
        sym_c = sympy.sympify(c)
        sym_m = sympy.sympify(m)
        sym_x = sympy.sympify(x)
        
        # A value x is a solution to u \equiv v \pmod m iff (u - v) / m is an integer
        val1 = (sym_a * sym_x - sym_b) / sym_m
        val2 = (sym_a * sym_c * sym_x - sym_b * sym_c) / sym_m
        
        sol1 = is_integer_val(val1)
        sol2 = is_integer_val(val2)
        
        # The conclusion is that sol1 == sol2. The negation is sol1 != sol2.
        neg_q = (sol1 != sol2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]