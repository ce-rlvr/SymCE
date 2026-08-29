import sympy
from sympy.abc import x, y

QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)):
            if sympy.isprime(witness):
                K = sympy.GF(witness)
                char = witness
                h1 = True
            else:
                K = None
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            K = witness
            if callable(K.characteristic):
                char = K.characteristic()
            else:
                char = K.characteristic
            h1 = True
        else:
            K = None
    except Exception:
        K = None

    if K is not None:
        try:
            h2 = bool(char != 2)
        except Exception:
            pass
            
        try:
            h3 = bool(char != 3)
        except Exception:
            pass
            
        try:
            poly = x**2 - x*y + y**2
            fac_list = sympy.factor_list(poly, domain=K)[1]
            if len(fac_list) > 1 or (len(fac_list) == 1 and fac_list[0][1] > 1):
                neg_q = True
            else:
                neg_q = False
        except Exception:
            pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K is not 2",
    "H_3: The characteristic of K is not 3",
    "¬Q: The polynomial is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3