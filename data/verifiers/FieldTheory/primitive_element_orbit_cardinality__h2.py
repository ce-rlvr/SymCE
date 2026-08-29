import sympy as sp
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension with Galois group G",
    "¬Q: E = F(alpha) is not equivalent to the orbit of alpha having cardinality equal to the degree of E over F"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # 1. Dictionary witness
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_finite_galois', False))
            orbit_card = witness.get('orbit_cardinality', None)
            deg = witness.get('degree', None)
            is_E_eq = witness.get('is_E_eq_F_alpha', None)
            if orbit_card is not None and deg is not None and is_E_eq is not None:
                neg_q = bool(is_E_eq != (orbit_card == deg))
                return [h1, neg_q]

        # 2. Object witness
        if hasattr(witness, 'is_finite_galois') and hasattr(witness, 'orbit_cardinality'):
            h1 = bool(getattr(witness, 'is_finite_galois', False))
            orbit_card = getattr(witness, 'orbit_cardinality', None)
            deg = getattr(witness, 'degree', None)
            is_E_eq = getattr(witness, 'is_E_eq_F_alpha', None)
            if orbit_card is not None and deg is not None and is_E_eq is not None:
                neg_q = bool(is_E_eq != (orbit_card == deg))
                return [h1, neg_q]

        # 3. Tuple witness
        if isinstance(witness, tuple) and len(witness) == 3:
            deg, orbit_card, is_E_eq = witness
            if isinstance(deg, int) and isinstance(orbit_card, int) and isinstance(is_E_eq, bool):
                h1 = (deg > 0)
                neg_q = bool(is_E_eq != (orbit_card == deg))
                return [h1, neg_q]

    except Exception:
        pass
        
    return [False, False]