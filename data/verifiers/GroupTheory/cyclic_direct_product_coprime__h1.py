import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic(grp):
    try:
        o = int(grp.order())
        if o == 1:
            return True
        for g in grp.elements:
            if int(g.order()) == o:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, m_wit, H, n_wit = witness
        else:
            G, H = witness[0], witness[1]
    except Exception:
        return [False, False, False, False]

    # H1: G is a cyclic group
    try:
        h1 = is_cyclic(G)
    except Exception:
        h1 = False

    # H2: H is a cyclic group
    try:
        h2 = is_cyclic(H)
    except Exception:
        h2 = False

    # H3: gcd(m, n) = 1
    try:
        m = int(G.order())
        n = int(H.order())
        h3 = math.gcd(m, n) == 1
    except Exception:
        h3 = False

    # neg_Q: G x H is NOT a cyclic group of order mn
    try:
        m = int(G.order())
        n = int(H.order())
        GxH = G * H
        q = is_cyclic(GxH) and int(GxH.order()) == m * n
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: H is a cyclic group",
    "H_3: gcd(|G|, |H|) = 1",
    "¬Q: G x H is not a cyclic group of order |G||H|"
]

N_HYP = 3
NEG_Q_INDEX = 3