import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a dictionary or object with the following properties:
      - is_commutative_noetherian_local_ring: bool
      - pd_M: int or float (projective dimension of M)
      - depth_M: int or float (depth of M)
      - depth_R: int or float (depth of R)
    """
    
    # H_1: (R, \mathfrak{m}) is a commutative Noetherian local ring
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_noetherian_local_ring', False))
        else:
            h1 = bool(getattr(witness, 'is_commutative_noetherian_local_ring', False))
    except Exception:
        h1 = False

    # H_2: The projective dimension of M over R is finite
    try:
        if isinstance(witness, dict):
            pd_M = witness.get('pd_M', float('inf'))
        else:
            pd_M = getattr(witness, 'pd_M', float('inf'))
        h2 = (pd_M is not None) and (pd_M < float('inf'))
    except Exception:
        h2 = False

    # ¬Q: pd_R(M) + depth_R(M) != depth(R)
    try:
        if isinstance(witness, dict):
            pd_M = witness.get('pd_M', None)
            depth_M = witness.get('depth_M', None)
            depth_R = witness.get('depth_R', None)
        else:
            pd_M = getattr(witness, 'pd_M', None)
            depth_M = getattr(witness, 'depth_M', None)
            depth_R = getattr(witness, 'depth_R', None)
            
        if pd_M is None or depth_M is None or depth_R is None:
            neg_q = False
        else:
            neg_q = (pd_M + depth_M) != depth_R
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "H_2: The projective dimension of M over R is finite",
    "¬Q: pd_R(M) + depth_R(M) != depth(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2