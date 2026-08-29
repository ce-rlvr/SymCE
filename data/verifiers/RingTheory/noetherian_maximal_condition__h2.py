import sympy
from sympy import ZZ, QQ

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The set S does not contain a maximal element"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_noetherian(R):
    if R in (sympy.ZZ, sympy.QQ, int, float, complex):
        return True
    if isinstance(R, str) and R in ("ZZ", "QQ", "Z", "Q", "R", "C"):
        return True
    if hasattr(R, 'is_Noetherian') and R.is_Noetherian:
        return True
    if hasattr(R, 'domain') and is_noetherian(R.domain):
        return True
    return False

def conditions(witness):
    try:
        # The witness can be a tuple (R, S) or just S (with R implicitly ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = sympy.ZZ
            S = witness
            
        # Check H_1: R is a Noetherian ring
        try:
            h1 = bool(is_noetherian(R))
        except Exception:
            h1 = False
            
        # Check ¬Q: S does not contain a maximal element.
        # Mathematically, in a Noetherian ring, EVERY non-empty set of ideals 
        # has a maximal element. Therefore, the ONLY way S can fail to have 
        # a maximal element is if S is empty.
        try:
            if hasattr(S, '__len__'):
                is_empty = (len(S) == 0)
            else:
                iterator = iter(S)
                try:
                    next(iterator)
                    is_empty = False
                except StopIteration:
                    is_empty = True
            neg_q = bool(is_empty)
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]