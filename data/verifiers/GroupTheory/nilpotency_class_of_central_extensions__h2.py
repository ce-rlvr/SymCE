import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    # The witness could be just a group G, or a tuple (G, c)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, c = witness
        else:
            G = witness
            c = None
    except Exception:
        G = witness
        c = None

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: G is not nilpotent of class c+1
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            is_nilp = getattr(G, 'is_nilpotent', None)
            if callable(is_nilp):
                is_nilp = is_nilp()
            
            if not is_nilp:
                # If G is not nilpotent, it is not nilpotent of class c+1 for any c
                neg_q_ok = True
            else:
                if c is not None:
                    nilp_class = getattr(G, 'nilpotency_class', None)
                    if callable(nilp_class):
                        nilp_class = nilp_class()
                    neg_q_ok = bool(nilp_class != c + 1)
                else:
                    # If c is not provided, since G has a specific nilpotency class k,
                    # the conclusion "G is nilpotent of class c+1" fails for any c != k-1.
                    # Thus, there exists a c for which the conclusion fails.
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: G is not nilpotent of class c+1"
]

N_HYP = 1
NEG_Q_INDEX = 1