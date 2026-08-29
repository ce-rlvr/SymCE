import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    # Extract G and p
    if isinstance(witness, tuple):
        if len(witness) != 2:
            return [False, False]
        G, p = witness
    else:
        G = witness
        try:
            order = G.order()
            if order % 2 != 0:
                p = None
            else:
                p = order // 2
        except Exception:
            p = None

    # H_1: G is a non-abelian finite group of order 2p
    try:
        if p is None:
            h1 = False
        else:
            h1 = getattr(G, 'is_abelian', True) is False and G.order() == 2 * p
    except Exception:
        h1 = False

    # ¬Q: The number of Sylow 2-subgroups of G is not exactly p
    try:
        if p is None:
            neg_q = False
        else:
            P = G.sylow_subgroup(2)
            P_elements = set(P.generate())
            n_G_P = 0
            for g in G.generate():
                is_normalizer = True
                for x in P.generators:
                    if (~g * x * g) not in P_elements:
                        is_normalizer = False
                        break
                if is_normalizer:
                    n_G_P += 1
            n_2 = G.order() // n_G_P
            neg_q = bool(n_2 != p)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian finite group of order 2p",
    "¬Q: The number of Sylow 2-subgroups of G is not exactly p"
]

N_HYP = 1
NEG_Q_INDEX = 1
