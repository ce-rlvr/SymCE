import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC, FF

GF = FF

def conditions(witness):
    # H_1: K is a field
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = sympy.isprime(int(witness))
        else:
            if hasattr(witness, 'is_Field') and witness.is_Field:
                if isinstance(witness, sympy.Expr):
                    h1 = False
                else:
                    h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: K is finite
    try:
        if isinstance(witness, (int, sympy.Integer)):
            neg_q = True
        else:
            name = type(witness).__name__
            neg_q = ('FiniteField' in name or 
                     'GaloisField' in name or 
                     name.startswith('FF_'))
            neg_q = bool(neg_q)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "¬Q: K is finite"
]

N_HYP = 1
NEG_Q_INDEX = 1