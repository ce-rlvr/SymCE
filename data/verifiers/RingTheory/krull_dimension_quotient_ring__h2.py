import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    h1 = False
    neg_q = False

    # Handle case where witness is a tuple, e.g., (R, I) or (R, R_mod_I)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        try:
            if isinstance(R, dict):
                h1 = bool(R.get('is_commutative', False))
                dim_R = R['dim_R']
            else:
                h1 = bool(getattr(R, 'is_commutative', False))
                dim_R = getattr(R, 'dim_R')
                
            if isinstance(I, dict):
                dim_R_mod_I = I.get('dim_R_mod_I', I.get('dim', I.get('dim_R', None)))
            else:
                dim_R_mod_I = getattr(I, 'dim_R_mod_I', getattr(I, 'dim', getattr(I, 'dim_R', None)))
                
            if dim_R_mod_I is not None:
                neg_q = bool(dim_R_mod_I > dim_R)
                return [h1, neg_q]
        except Exception:
            pass

    # Handle case where witness is a single object or dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', False))
        else:
            h1 = bool(getattr(witness, 'is_commutative', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            dim_R = witness['dim_R']
            dim_R_mod_I = witness['dim_R_mod_I']
        else:
            dim_R = getattr(witness, 'dim_R')
            dim_R_mod_I = getattr(witness, 'dim_R_mod_I')
        neg_q = bool(dim_R_mod_I > dim_R)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The Krull dimension of the quotient ring R/I is greater than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1