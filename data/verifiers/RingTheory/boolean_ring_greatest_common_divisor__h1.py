import sympy
import math
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: a and b are elements of a ring R",
    "¬Q: a + b + ab is not a greatest common divisor of a and b in R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, list):
            witness = tuple(witness)
            
        if not isinstance(witness, tuple):
            return [False, False]
            
        if len(witness) == 2:
            a, b = witness
            if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
                h1 = True
                a_val = int(a)
                b_val = int(b)
                d = a_val + b_val + a_val * b_val
                is_gcd = (abs(d) == math.gcd(a_val, b_val))
                neg_q = not is_gcd
                return [h1, neg_q]
            else:
                h1 = True
                d = a + b + a * b
                try:
                    def divides_poly(p1, p2):
                        if p1 == 0:
                            return p2 == 0
                        try:
                            q, r = sympy.div(p2, p1)
                            return r == 0
                        except Exception:
                            return False

                    if not divides_poly(d, a) or not divides_poly(d, b):
                        is_gcd = False
                    else:
                        actual_gcd = sympy.gcd(a, b)
                        is_gcd = divides_poly(d, actual_gcd) and divides_poly(actual_gcd, d)
                    neg_q = not is_gcd
                    return [h1, neg_q]
                except Exception:
                    return [False, False]
                    
        elif len(witness) == 3:
            n, a, b = witness
            if isinstance(n, (int, sympy.Integer)) and isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
                n_val = int(n)
                if n_val < 2:
                    return [False, False]
                h1 = True
                a_mod = int(a) % n_val
                b_mod = int(b) % n_val
                d = (a_mod + b_mod + a_mod * b_mod) % n_val
                
                def divides(x_val, y_val):
                    for k in range(n_val):
                        if (x_val * k) % n_val == y_val % n_val:
                            return True
                    return False
                
                is_gcd = True
                if not divides(d, a_mod) or not divides(d, b_mod):
                    is_gcd = False
                else:
                    for c in range(n_val):
                        if divides(c, a_mod) and divides(c, b_mod):
                            if not divides(c, d):
                                is_gcd = False
                                break
                neg_q = not is_gcd
                return [h1, neg_q]
                
    except Exception:
        pass
        
    return [False, False]