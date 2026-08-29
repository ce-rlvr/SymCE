import math
import itertools
import functools
import z3
import sympy
from sympy import oo
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "¬Q: The external semidirect product is not a finite group of order |N| * |H|"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: phi is a group homomorphism
    h1 = False
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_homomorphism', witness.get('is_hom', False)))
        elif isinstance(witness, tuple) and len(witness) >= 4:
            h1 = bool(witness[3])
        elif hasattr(witness, 'is_homomorphism'):
            h1 = bool(witness.is_homomorphism() if callable(witness.is_homomorphism) else witness.is_homomorphism)
        elif hasattr(witness, 'is_hom'):
            h1 = bool(witness.is_hom() if callable(witness.is_hom) else witness.is_hom)
    except Exception:
        pass

    # neg_Q: The external semidirect product is NOT a finite group of order |N| * |H|
    neg_q = False
    try:
        if isinstance(witness, dict):
            if not all(k in witness for k in ('sdp_order', 'N_order', 'H_order')):
                return [h1, False]
            sdp_order = witness['sdp_order']
            N_order = witness['N_order']
            H_order = witness['H_order']
        elif isinstance(witness, tuple) and len(witness) >= 3:
            N_order = witness[0]
            H_order = witness[1]
            sdp_order = witness[2]
        else:
            if hasattr(witness, 'sdp_order'):
                sdp_order = witness.sdp_order() if callable(witness.sdp_order) else witness.sdp_order
            else:
                sdp_order = witness.order()

            if hasattr(witness, 'N_order'):
                N_order = witness.N_order() if callable(witness.N_order) else witness.N_order
            else:
                N_order = witness.N.order()

            if hasattr(witness, 'H_order'):
                H_order = witness.H_order() if callable(witness.H_order) else witness.H_order
            else:
                H_order = witness.H.order()

        def is_fin(ord_val):
            if ord_val is None: 
                return False
            if ord_val == oo or ord_val == math.inf or ord_val == float('inf'):
                return False
            if isinstance(ord_val, str) and 'inf' in ord_val.lower():
                return False
            return True

        sdp_finite = is_fin(sdp_order)
        
        if sdp_finite:
            if not is_fin(N_order) or not is_fin(H_order):
                conclusion = False
            else:
                conclusion = (sdp_order == N_order * H_order)
        else:
            conclusion = False

        neg_q = not conclusion

    except Exception:
        neg_q = False

    return [h1, neg_q]