import math
import sympy
from sympy import Rational

def v2(val):
    if val == 0:
        return math.inf
    try:
        val = sympy.simplify(val)
        q = Rational(val)
    except Exception:
        return None
    
    num = q.p
    den = q.q
    
    def v2_int(k):
        if k == 0: return math.inf
        ans = 0
        while k % 2 == 0:
            ans += 1
            k //= 2
        return ans

    return v2_int(num) - v2_int(den)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
            n = witness.get('n')
        else:
            x, y, n = witness
    except Exception:
        return [False, False, False]

    # H_1: x and y are odd integers
    try:
        x_rat = Rational(x)
        y_rat = Rational(y)
        h1 = bool((x_rat.q == 1) and (y_rat.q == 1) and (x_rat.p % 2 != 0) and (y_rat.p % 2 != 0))
    except Exception:
        h1 = False

    # H_2: x - y is a multiple of 4
    try:
        x_rat = Rational(x)
        y_rat = Rational(y)
        h2 = bool((x_rat.p - y_rat.p) % 4 == 0)
    except Exception:
        h2 = False

    # neg_Q: v_2(x^n - y^n) != v_2(x-y) + v_2(n)
    try:
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        n_sym = sympy.sympify(n)
        
        val1_sym = x_sym**n_sym - y_sym**n_sym
        v2_val1 = v2(val1_sym)
        
        val2_sym = x_sym - y_sym
        v2_val2 = v2(val2_sym)
        
        v2_n = v2(n_sym)
        
        if v2_val1 is None or v2_val2 is None or v2_n is None:
            neg_q = False
        else:
            neg_q = bool(v2_val1 != v2_val2 + v2_n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are odd integers",
    "H_2: x - y is a multiple of 4",
    "¬Q: v_2(x^n - y^n) != v_2(x-y) + v_2(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2