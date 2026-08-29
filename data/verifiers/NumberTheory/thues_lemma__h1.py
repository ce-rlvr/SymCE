import math
import sympy

# Top-level setup
# No specific named objects required for this number theory conjecture.

def is_integer(x):
    if isinstance(x, int):
        return True
    if isinstance(x, sympy.Integer):
        return True
    return False

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        a, n = witness
    except Exception:
        return [False, False]
    
    try:
        if not (is_integer(a) and is_integer(n)):
            h1 = False
        else:
            a_int = int(a)
            n_int = int(n)
            h1 = math.gcd(a_int, n_int) == 1
    except Exception:
        h1 = False
        
    try:
        if not (is_integer(a) and is_integer(n)):
            neg_q = False
        else:
            a_int = int(a)
            n_int = int(n)
            if n_int < 0:
                neg_q = True
            else:
                limit = math.floor(math.sqrt(n_int))
                conclusion_holds = False
                for x in range(1, limit + 1):
                    if n_int == 0:
                        y = a_int * x
                        if y != 0 and abs(y) <= limit:
                            conclusion_holds = True
                            break
                    else:
                        rem = (a_int * x) % n_int
                        for y in (rem, rem - n_int, rem + n_int):
                            if y != 0 and abs(y) <= limit:
                                conclusion_holds = True
                                break
                    if conclusion_holds:
                        break
                neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer coprime to n",
    "¬Q: There do not exist integers x, y with 0 < |x| <= sqrt(n), 0 < |y| <= sqrt(n) such that ax = y (mod n)"
]

N_HYP = 1
NEG_Q_INDEX = 1