import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the Auslander-Buchsbaum Formula conjecture.
    The witness is expected to be a dictionary containing the properties of the ring R and module M.
    """
    try:
        # H_1: M is a non-zero finitely generated R-module
        h1 = bool(witness['is_nonzero']) and bool(witness['is_fg'])
    except Exception:
        h1 = False

    try:
        # H_2: The projective dimension of M over R is finite
        pd = witness['pd_M']
        h2 = pd != sympy.oo and pd >= 0
    except Exception:
        h2 = False

    try:
        # ¬Q: The sum of the projective dimension of M and the depth of M is NOT equal to the depth of the ring R
        pd = witness['pd_M']
        depth_M = witness['depth_M']
        depth_R = witness['depth_R']
        neg_q = (pd + depth_M) != depth_R
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a non-zero finitely generated R-module",
    "H_2: The projective dimension of M over R is finite",
    "¬Q: pd_R(M) + depth(M) != depth(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2