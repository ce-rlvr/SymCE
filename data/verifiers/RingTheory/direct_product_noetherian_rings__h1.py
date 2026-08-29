import sympy
from sympy import S
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.domains.domain import Domain

# Top-level setup for potential witness expressions
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

def is_commutative_ring(R):
    if isinstance(R, Domain):
        return True
    if isinstance(R, int) and R > 1:
        return True
    if isinstance(R, str) and R in ["ZZ", "QQ", "RR", "CC"]:
        return True
    if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
        return True
    return False

def is_noetherian(R):
    if isinstance(R, str):
        if R in ["ZZ", "QQ", "RR", "CC"]:
            return True
        return False
        
    if isinstance(R, int) and R > 1:
        return True
        
    if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
        return True
        
    if isinstance(R, Domain):
        if R in (ZZ, QQ, RR, CC):
            return True
        if getattr(R, 'is_Field', False):
            return True
        if hasattr(R, 'domain') and hasattr(R, 'symbols'):
            return is_noetherian(R.domain)
            
    return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)):
            h1 = False
        else:
            h1 = all(is_commutative_ring(R) for R in witness)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(witness, (list, tuple)):
            h2 = False
        else:
            h2 = all(is_noetherian(R) for R in witness)
    except Exception:
        h2 = False
        
    try:
        if not isinstance(witness, (list, tuple)):
            neg_q = False
        elif not all(is_commutative_ring(R) for R in witness):
            neg_q = False
        else:
            # The direct product of rings is Noetherian if and only if all factors are Noetherian.
            # Thus, the direct product is NOT Noetherian iff not all factors are Noetherian.
            neg_q = not all(is_noetherian(R) for R in witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The witness is a finite collection of commutative rings",
    "H_2: Each ring in the collection is a Noetherian ring",
    "¬Q: The direct product of the rings in the collection is NOT a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2