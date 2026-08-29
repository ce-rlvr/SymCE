import sympy
import itertools
import math
from sympy.abc import x, y, z

def divides(x_val, y_val):
    if x_val == 0:
        return y_val == 0
    if x_val == 1 or x_val == -1:
        return True
    try:
        if isinstance(x_val, int) and isinstance(y_val, int):
            return y_val % x_val == 0
    except Exception:
        pass
    try:
        x_sym = sympy.sympify(x_val)
        y_sym = sympy.sympify(y_val)
        if x_sym == 0:
            return y_sym == 0
        ratio = sympy.cancel(y_sym / x_sym)
        num, den = ratio.as_numer_denom()
        if den == 1 or den == -1:
            return True
        if den.is_number and den != 0:
            return True
    except Exception:
        pass
    return False

def get_sympy_divisors(expr):
    if expr == 0:
        return []
    try:
        unit, factors = sympy.factor_list(expr)
        divs = []
        bases = [f[0] for f in factors]
        exps = [f[1] for f in factors]
        ranges = [range(e + 1) for e in exps]
        for powers in itertools.product(*ranges):
            d = unit
            for b, p in zip(bases, powers):
                d *= b**p
            divs.append(d)
        return divs
    except Exception:
        return []

def conditions(witness):
    if isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            a, b, c = witness
            R = None
        elif len(witness) == 4:
            R, a, b, c = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]
        
    # H_1: Let R be a Unique Factorization Domain
    try:
        if R is not None:
            if hasattr(R, 'is_UFD'):
                h1 = bool(R.is_UFD)
            else:
                h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False
        
    # H_2: The element a divides the product bc
    try:
        bc = b * c
        h2 = divides(a, bc)
    except Exception:
        h2 = False
        
    # Conclusion: There exist elements a_1, a_2 in R such that a = a_1 * a_2, where a_1 divides b and a_2 divides c
    q_holds = False
    try:
        if isinstance(a, int) and isinstance(b, int) and isinstance(c, int):
            if a == 0:
                if b == 0 or c == 0:
                    q_holds = True
            else:
                divs = sympy.divisors(abs(a))
                divs = divs + [-d for d in divs]
                for a1 in divs:
                    if a % a1 == 0:
                        a2 = a // a1
                        if divides(a1, b) and divides(a2, c):
                            q_holds = True
                            break
        else:
            a_sym = sympy.sympify(a)
            b_sym = sympy.sympify(b)
            c_sym = sympy.sympify(c)
            if a_sym == 0:
                if b_sym == 0 or c_sym == 0:
                    q_holds = True
            else:
                # Try the standard gcd construction first
                a1 = sympy.gcd(a_sym, b_sym)
                a2 = sympy.cancel(a_sym / a1)
                if divides(a1, b_sym) and divides(a2, c_sym):
                    if sympy.simplify(a1 * a2 - a_sym) == 0:
                        q_holds = True
                
                # Fallback to exhaustive divisor search
                if not q_holds:
                    divs = get_sympy_divisors(a_sym)
                    for a1 in divs:
                        a2 = sympy.cancel(a_sym / a1)
                        if divides(a1, b_sym) and divides(a2, c_sym):
                            if sympy.simplify(a1 * a2 - a_sym) == 0:
                                q_holds = True
                                break
    except Exception:
        q_holds = False
        
    neg_q = not q_holds
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: The element a divides the product bc",
    "¬Q: There do not exist elements a_1, a_2 in R such that a = a_1 * a_2, where a_1 divides b and a_2 divides c"
]

N_HYP = 2
NEG_Q_INDEX = 2