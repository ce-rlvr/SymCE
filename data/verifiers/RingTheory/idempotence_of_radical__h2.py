import sympy
from sympy.ntheory import factorint
from sympy.abc import x, y, z

def rad(n):
    try:
        if isinstance(n, (int, sympy.Integer)):
            factors = factorint(n)
            res = 1
            for p in factors:
                res *= p
            return res
    except Exception:
        pass
    if hasattr(n, 'radical'):
        r = n.radical
        return r() if callable(r) else r
    if hasattr(n, 'rad'):
        r = n.rad
        return r() if callable(r) else r
    return n

def conditions(witness):
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', True))
            I = witness.get('I', None)
            if I is not None and 'rad_I' not in witness:
                rad_I = rad(I)
                rad_rad_I = rad(rad_I)
            else:
                rad_I = witness.get('rad_I')
                rad_rad_I = witness.get('rad_rad_I')
            neg_q = bool(rad_rad_I != rad_I)
            return [h1, neg_q]
            
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R, I = witness, witness
            
        if hasattr(R, 'is_commutative'):
            c = R.is_commutative
            h1 = bool(c() if callable(c) else c)
        else:
            h1 = True
            
        rad_I = rad(I)
        rad_rad_I = rad(rad_I)
        
        if hasattr(rad_rad_I, 'equals') and callable(rad_rad_I.equals):
            eq = rad_rad_I.equals(rad_I)
            if eq is not None:
                neg_q = not eq
            else:
                neg_q = bool(rad_rad_I != rad_I)
        else:
            neg_q = bool(rad_rad_I != rad_I)
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The radical of the radical of I is not equal to the radical of I"
]

N_HYP = 1
NEG_Q_INDEX = 1