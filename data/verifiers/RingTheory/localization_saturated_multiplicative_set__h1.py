import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Since the counterexample must be an infinite non-commutative ring (as finite rings 
    are Dedekind-finite and thus their localizations are always isomorphic), 
    the witness is expected to provide its properties via methods or dictionary keys.
    """
    # H_1: S is a multiplicatively closed subset of R
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_multiplicatively_closed', False))
        else:
            h1 = bool(witness.is_multiplicatively_closed())
    except Exception:
        h1 = False

    # H_2: \bar{S} is the saturation of S
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_saturation', False))
        else:
            h2 = bool(witness.is_saturation())
    except Exception:
        h2 = False

    # ¬Q: The localized rings S^{-1}R and \bar{S}^{-1}R are NOT canonically isomorphic
    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get('are_canonically_isomorphic', True))
        else:
            neg_q = not bool(witness.are_canonically_isomorphic())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: \\bar{S} is the saturation of S",
    "¬Q: The localized rings S^{-1}R and \\bar{S}^{-1}R are not canonically isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2