import sympy
from sympy import ZZ, QQ
from sympy.abc import x
from sympy.polys.domains import Domain

# Top-level setup for witness evaluation
# A valid witness is a tuple (R, I_gen) where R is a SymPy Domain (e.g., ZZ, QQ[x])
# and I_gen is the generator of the ideal I.

def conditions(witness):
    try:
        R, I_gen = witness
    except Exception:
        return [False, False]
    
    try:
        # H_1: R is a Euclidean domain and I is an ideal of R.
        # In SymPy, ZZ and K[x] are PIDs. Since all Euclidean domains are PIDs, 
        # and the standard PIDs in SymPy are Euclidean, we use is_PID as a proxy.
        is_domain = isinstance(R, Domain)
        is_euclidean = is_domain and getattr(R, 'is_PID', False)
        h1 = bool(is_euclidean and I_gen in R)
    except Exception:
        h1 = False

    try:
        # ¬Q: R/I is NOT an Artinian ring.
        # For a PID R, the quotient R/I is Artinian if and only if R is a field or I != 0.
        # Therefore, R/I is NOT Artinian if and only if R is not a field and I == 0.
        is_field = getattr(R, 'is_Field', False)
        is_zero = (I_gen == getattr(R, 'zero', 0) or I_gen == 0)
        neg_q = bool((not is_field) and is_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain and I is an ideal of R",
    "¬Q: R/I is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1