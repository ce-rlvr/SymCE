import sympy
from sympy.polys.domains.ring import Ring
from sympy.polys.domains.field import Field

# Top-level setup for Ring/Field domain
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # H_1: Let R be a commutative ring with identity
    try:
        h1 = False
        if isinstance(witness, (Ring, Field)):
            h1 = True
        elif getattr(witness, 'is_ring', False) and getattr(witness, 'is_commutative', False) and getattr(witness, 'has_identity', False):
            h1 = True
    except Exception:
        h1 = False

    # H_2: Let Spec(R) denote the set of all prime ideals of R
    # This is a definitional hypothesis, inherently true for any valid ring context.
    try:
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The topological space Spec(R) is NOT quasi-compact
    # Mathematically, the prime spectrum of ANY commutative ring with identity 
    # is always quasi-compact. Therefore, the conclusion never fails for a valid witness.
    try:
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Spec(R) denotes the set of all prime ideals of R",
    "¬Q: The topological space Spec(R) is not quasi-compact"
]

N_HYP = 2
NEG_Q_INDEX = 2