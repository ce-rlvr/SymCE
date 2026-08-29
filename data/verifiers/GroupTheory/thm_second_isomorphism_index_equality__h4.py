import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, N = witness
        else:
            G = witness
            H = getattr(witness, 'H', None)
            N = getattr(witness, 'N', None)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        if hasattr(G, 'is_group'):
            h1 = G.is_group() if callable(G.is_group) else bool(G.is_group)
        elif isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = H.is_subgroup(G) if callable(H.is_subgroup) else bool(H.is_subgroup)
        elif isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = H.is_subgroup(G)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        if hasattr(N, 'is_normal'):
            h3 = N.is_normal(G) if callable(N.is_normal) else bool(N.is_normal)
        elif hasattr(N, 'is_normal_subgroup'):
            h3 = N.is_normal_subgroup(G) if callable(N.is_normal_subgroup) else bool(N.is_normal_subgroup)
        elif isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            h3 = N.is_normal(G)
        else:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: The index of N in HN is not finite or not equal to the index of H cap N in H
    try:
        idx_HN_N = None
        idx_H_HcapN = None

        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(N, PermutationGroup):
            HN_gens = list(H.generators) + list(N.generators)
            HN = PermutationGroup(HN_gens)
            H_cap_N = H.intersection(N)
            idx_HN_N = HN.order() / N.order()
            idx_H_HcapN = H.order() / H_cap_N.order()
        else:
            if hasattr(G, 'idx_HN_N'):
                idx_HN_N = G.idx_HN_N(H, N) if callable(G.idx_HN_N) else G.idx_HN_N
            elif hasattr(witness, 'idx_HN_N'):
                idx_HN_N = witness.idx_HN_N() if callable(witness.idx_HN_N) else witness.idx_HN_N

            if hasattr(G, 'idx_H_HcapN'):
                idx_H_HcapN = G.idx_H_HcapN(H, N) if callable(G.idx_H_HcapN) else G.idx_H_HcapN
            elif hasattr(witness, 'idx_H_HcapN'):
                idx_H_HcapN = witness.idx_H_HcapN() if callable(witness.idx_H_HcapN) else witness.idx_H_HcapN

        if idx_HN_N is None or idx_H_HcapN is None:
            if hasattr(witness, 'Q_holds'):
                Q = witness.Q_holds() if callable(witness.Q_holds) else bool(witness.Q_holds)
                neg_q = not Q
            elif hasattr(G, 'Q_holds'):
                Q = G.Q_holds(H, N) if callable(G.Q_holds) else bool(G.Q_holds)
                neg_q = not Q
            else:
                neg_q = False
        else:
            is_finite = (idx_HN_N != oo) and (idx_HN_N != float('inf'))
            is_equal = (idx_HN_N == idx_H_HcapN)
            Q = is_finite and is_equal
            neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N is a normal subgroup of G",
    "¬Q: The index of N in HN is not finite or not equal to the index of H cap N in H"
]

N_HYP = 3
NEG_Q_INDEX = 3