import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            n = int(witness)
            h1 = (n >= 1)
            G = AlternatingGroup(n) if h1 else None
        elif hasattr(witness, 'degree') and hasattr(witness, 'order') and hasattr(witness, 'generators'):
            G = witness
            n = G.degree
            expected_order = math.factorial(n) // 2 if n >= 2 else 1
            order_val = G.order() if callable(G.order) else G.order
            h1 = (order_val == expected_order) and all(getattr(p, 'is_even', False) for p in G.generators)
        else:
            h1 = False
            G = None
            n = None
    except Exception:
        h1 = False
        G = None
        n = None

    try:
        if G is not None and h1:
            # A_n is simple if and only if n >= 5 or n == 3
            is_simple = (n >= 5 or n == 3)
            neg_q = not is_simple
        elif G is not None:
            # Fallback for other permutation groups
            if hasattr(G, 'is_simple') and callable(G.is_simple):
                is_simple = G.is_simple()
            elif hasattr(G, 'is_simple') and isinstance(G.is_simple, bool):
                is_simple = G.is_simple
            else:
                ns = list(G.normal_subgroups())
                is_simple = (len(ns) == 2)
            neg_q = not is_simple
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A_n is the alternating group of degree n",
    "¬Q: A_n is not a simple group"
]

N_HYP = 1
NEG_Q_INDEX = 1