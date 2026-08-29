import sympy
import math
from sympy.abc import x, y, z

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, a, b = witness
                # Handle the case where the ring is explicitly Z/nZ
                if isinstance(R, (int, sympy.Integer)) and R >= 2 and isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
                    h1 = True
                    h2 = True
                    da = math.gcd(int(a), int(R))
                    db = math.gcd(int(b), int(R))
                    L = (da * db) // math.gcd(da, db)
                    P = math.gcd(int(a * b), int(R))
                    neg_q = (L != P)
                    return [h1, h2, neg_q]
                else:
                    h1 = True
                    h2 = True
            elif len(witness) == 2:
                a, b = witness
                h1 = True
                h2 = True
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        # Handle elements in ZZ
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            h1 = True
            h2 = True
            L = sympy.lcm(a, b)
            P = a * b
            neg_q = abs(L) != abs(P)
            
        # Handle elements in polynomial rings (e.g., QQ[x])
        elif isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr):
            h1 = True
            h2 = getattr(a, 'is_commutative', True) and getattr(b, 'is_commutative', True)
            if not h2:
                return [h1, h2, False]
            
            L = sympy.lcm(a, b)
            P = sympy.expand(a * b)
            
            if P == 0:
                neg_q = (L != 0)
            elif L == 0:
                neg_q = True
            else:
                q1, r1 = sympy.div(L, P)
                q2, r2 = sympy.div(P, L)
                same_ideal = (r1 == 0) and (r2 == 0)
                neg_q = not same_ideal
        else:
            h1 = False
            h2 = False
            neg_q = False
            
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: a and b are elements of R",
    "¬Q: The intersection of the principal ideals (a) and (b) is not equal to the principal ideal (ab)"
]

N_HYP = 2
NEG_Q_INDEX = 2