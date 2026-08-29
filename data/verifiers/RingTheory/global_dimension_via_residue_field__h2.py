import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

class LocalRingProfile:
    """
    A profile representing a mathematical ring for the purpose of verifying
    homological properties that cannot be directly computed in SymPy.
    """
    def __init__(self, is_commutative, is_local, global_dimension, projective_dimension_k):
        self.is_commutative = is_commutative
        self.is_local = is_local
        self.global_dimension = global_dimension
        self.projective_dimension_k = projective_dimension_k

# Standard algebra objects
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
    try:
        if isinstance(witness, dict):
            is_comm = witness.get('is_commutative', False)
            is_loc = witness.get('is_local', False)
        else:
            is_comm = getattr(witness, 'is_commutative', False)
            is_loc = getattr(witness, 'is_local', False)
        h1 = bool(is_comm and is_loc)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            gldim = witness.get('global_dimension')
            pdk = witness.get('projective_dimension_k')
        else:
            gldim = getattr(witness, 'global_dimension', None)
            pdk = getattr(witness, 'projective_dimension_k', None)
        
        if gldim is None or pdk is None:
            neg_q = False
        else:
            neg_q = bool(gldim != pdk)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring with maximal ideal m",
    "¬Q: The global dimension of R is not equal to the projective dimension of k as an R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1