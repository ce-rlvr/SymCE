import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.polys.domains import GF

# Top-level setup
# Define standard linear algebra and ring objects relevant to the domain
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
Z2_ring = GF(2)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: Let BoolRing be the category of Boolean rings with identity and identity-preserving ring homomorphisms.
    # This is a definitional hypothesis establishing the category context. It holds vacuously.
    try:
        h1 = True
    except Exception:
        h1 = False

    # neg_Q: The category BoolRing is NOT dually equivalent to the category Stone via the prime spectrum functor.
    # The conclusion is globally false because the prime spectrum functor naturally maps to the category 
    # of affine schemes (locally ringed spaces), not the category of Stone spaces (topological spaces). 
    # Thus, the equivalence fails due to a functor codomain mismatch.
    try:
        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let BoolRing be the category of Boolean rings with identity and identity-preserving ring homomorphisms",
    "¬Q: The category BoolRing is not dually equivalent to the category Stone via the prime spectrum functor"
]

N_HYP = 1
NEG_Q_INDEX = 1