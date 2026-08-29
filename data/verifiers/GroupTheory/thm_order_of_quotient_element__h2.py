import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G with finite order k",
    "¬Q: The order of the coset gN in the quotient group G/N does not divide k (or G/N is not a valid quotient group)"
]

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            g = witness.get('g')
        else:
            G, N, g = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: g is an element of G with finite order k
    try:
        h2_ok = g in G
        k = g.order()
        if k <= 0:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The order of the coset gN in the quotient group G/N does not divide k
    # If N is not a normal subgroup, G/N is not a quotient group, so the conclusion fails (neg_Q is True).
    try:
        if not hasattr(N, 'is_subgroup') or not N.is_subgroup(G):
            neg_q_ok = True
        elif not G.is_normal(N):
            neg_q_ok = True
        else:
            k = g.order()
            m = 1
            curr = g
            while curr not in N:
                curr = curr * g
                m += 1
            neg_q_ok = (k % m != 0)
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]