import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math

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

def conditions(witness):
    # H_1: Let n be an integer such that n >= 2.
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            h1 = bool(witness >= 2)
    except Exception:
        h1 = False

    # H_2: Let A_n be the alternating group of degree n.
    # This is a definitional hypothesis; we verify n is a valid degree.
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h2 = False
        else:
            h2 = bool(witness >= 1)
    except Exception:
        h2 = False

    # ¬Q: The index of A_n in S_n is exactly 2, and A_n is a normal subgroup of S_n. (Must FAIL)
    try:
        if not isinstance(witness, (int, sympy.Integer)) or witness < 1:
            neg_q = False
        else:
            n = int(witness)
            Sn = SymmetricGroup(n)
            An = AlternatingGroup(n)
            
            index = Sn.order() // An.order()
            
            if hasattr(An, 'is_normal'):
                is_normal = bool(An.is_normal(Sn))
            else:
                is_normal = True
                for g in Sn.generators:
                    for h in An.generators:
                        conj = g * h * (g**-1)
                        if not An.contains(conj):
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            q = (index == 2) and is_normal
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "H_2: A_n is the alternating group of degree n",
    "¬Q: The index of A_n in S_n is not 2, or A_n is not a normal subgroup of S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2