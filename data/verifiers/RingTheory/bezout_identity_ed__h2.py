import sympy
from sympy import Rational

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: The greatest common divisor of a and b does not exist or cannot be written as ax + by for some x, y in R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, a, b = witness
            elif len(witness) == 2:
                R = sympy.ZZ
                a, b = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        # H1: R is a Euclidean domain
        h1 = False
        R_domain = None
        
        if R in (sympy.ZZ, sympy.S.Integers):
            h1 = True
            R_domain = sympy.ZZ
        elif R in (sympy.QQ, sympy.S.Rationals):
            h1 = True
            R_domain = sympy.QQ
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
            R_domain = R
            
        # neg_Q: gcd(a, b) does not exist OR cannot be written as ax + by for x, y in R
        # In a Euclidean domain, Bezout's identity always holds for elements IN the domain.
        # Thus, the conclusion fails iff a or b is NOT in R.
        neg_q = False
        if R_domain is not None:
            try:
                R_domain(a)
                R_domain(b)
            except Exception:
                neg_q = True
        else:
            # If R is not recognized as a Euclidean domain, we default neg_q to True
            # since we cannot verify membership or Bezout's identity.
            neg_q = True
            
        return [h1, neg_q]
    except Exception:
        return [False, False]