import sympy
from sympy import Poly
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x
import math

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
    if isinstance(witness, dict):
        try:
            n = witness.get('n', witness.get('degree', 0))
            h1 = witness.get('is_separable', witness.get('separable', False))
            h2 = witness.get('is_splitting_field', witness.get('splitting_field', True))
            h3 = witness.get('galois_is_Sn', witness.get('isomorphic_to_Sn', False))
            ext_deg = witness.get('extension_degree', witness.get('degree_E_F', 0))
            neg_q = ext_deg != math.factorial(int(n))
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        except Exception:
            pass

    try:
        if hasattr(witness, 'is_separable') or hasattr(witness, 'separable'):
            n = getattr(witness, 'n', getattr(witness, 'degree', 0))
            h1 = getattr(witness, 'is_separable', getattr(witness, 'separable', False))
            h2 = getattr(witness, 'is_splitting_field', getattr(witness, 'splitting_field', True))
            h3 = getattr(witness, 'galois_is_Sn', getattr(witness, 'isomorphic_to_Sn', False))
            ext_deg = getattr(witness, 'extension_degree', getattr(witness, 'degree_E_F', 0))
            neg_q = ext_deg != math.factorial(int(n))
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    if isinstance(witness, tuple) and len(witness) == 2:
        try:
            n, ext_deg = witness
            neg_q = ext_deg != math.factorial(int(n))
            return [True, True, True, bool(neg_q)]
        except Exception:
            pass

    return [False, False, False, False]

CONDITION_LABELS = ["H_1: f(x) is a separable polynomial over F of degree n", "H_2: E is the splitting field of f(x) over F", "H_3: The Galois group Gal(E over F) is isomorphic to the symmetric group S_n", "¬Q: The degree of the extension E over F is not equal to n!"]
N_HYP = 3
NEG_Q_INDEX = 3