import sympy
from sympy.polys.domains import QQ, RR, CC, ZZ, GF

def conditions(witness) -> list[bool]:
    # H_1: K is a field
    try:
        h1 = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    # ¬Q: W(K) is not isomorphic to Z/2Z
    try:
        s = str(witness)
        # W(K) is Z/2Z for algebraically closed fields (like CC) 
        # and perfect fields of characteristic 2 (like GF(2)).
        if s.startswith('CC'):
            witt_is_z2 = True
        elif s.startswith('RR') or s.startswith('QQ'):
            witt_is_z2 = False
        elif getattr(witness, 'is_FiniteField', False):
            witt_is_z2 = (witness.char == 2)
        else:
            # For other typical fields in SymPy (e.g. algebraic extensions of QQ, 
            # rational function fields, finite fields of odd characteristic), 
            # the Witt ring is not Z/2Z.
            witt_is_z2 = False
            
        neg_q = not witt_is_z2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "¬Q: W(K) is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1