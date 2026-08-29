import sympy
from sympy.ntheory import primefactors

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        elif isinstance(witness, dict):
            if 'n' in witness and 'x' in witness:
                R, x = witness['n'], witness['x']
            elif 'R' in witness and 'x' in witness:
                R, x = witness['R'], witness['x']
            elif 'ring' in witness and 'element' in witness:
                R, x = witness['ring'], witness['element']
            else:
                R, x = None, None
        else:
            R, x = None, None
            
        if R is sympy.ZZ or R is sympy.QQ:
            h1 = True
        else:
            R_int = int(R)
            h1 = (R_int >= 2)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        elif isinstance(witness, dict):
            if 'n' in witness and 'x' in witness:
                R, x = witness['n'], witness['x']
            elif 'R' in witness and 'x' in witness:
                R, x = witness['R'], witness['x']
            elif 'ring' in witness and 'element' in witness:
                R, x = witness['ring'], witness['element']
            else:
                R, x = None, None
        else:
            R, x = None, None
            
        if R is sympy.ZZ or R is sympy.QQ:
            neg_q = (x == 0)
        else:
            R_int = int(R)
            x_int = int(x)
            if R_int < 2:
                neg_q = False
            else:
                factors = primefactors(R_int)
                neg_q = all(x_int % p == 0 for p in factors)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: For all prime ideals P of R, x is an element of P"
]

N_HYP = 1
NEG_Q_INDEX = 1