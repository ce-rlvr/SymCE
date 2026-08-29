import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A3 = AlternatingGroup(3)
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
    G = None
    
    # Check H_1: witness is an integer n >= 1 or the alternating group A_n
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 1:
                h1 = True
                G = AlternatingGroup(n)
        else:
            G = witness
            if hasattr(G, 'degree') and hasattr(G, 'order') and hasattr(G, 'is_subgroup'):
                n = G.degree
                expected_order = math.factorial(n) // 2 if n >= 2 else 1
                if G.order() == expected_order and G.is_subgroup(AlternatingGroup(n)):
                    h1 = True
    except Exception:
        h1 = False

    # Check neg_Q: The center of A_n contains more than just the identity permutation
    neg_q = False
    if h1 and G is not None:
        try:
            C = G.center()
            if hasattr(C, 'order'):
                neg_q = C.order() > 1
            else:
                neg_q = len(list(C)) > 1
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is an integer n >= 1 or the alternating group A_n",
    "¬Q: The center of A_n contains more than just the identity permutation"
]

N_HYP = 1
NEG_Q_INDEX = 1