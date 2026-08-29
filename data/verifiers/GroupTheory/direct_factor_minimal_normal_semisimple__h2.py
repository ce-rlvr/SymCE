import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        G, M = witness
    except Exception:
        return [False, False]

    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            if G.order() == 1:
                h1 = True
            else:
                ns = G.normal_subgroups()
                if not any(N.order() > 1 and N.is_abelian for N in ns):
                    simple_normals = [N for N in ns if N.order() > 1 and len(N.normal_subgroups()) == 2]
                    gens = []
                    for N in simple_normals:
                        gens.extend(N.generators)
                    if gens:
                        h1 = PermutationGroup(gens).order() == G.order()
    except Exception:
        h1 = False

    try:
        neg_q = True
        if isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup):
            if M.is_subgroup(G):
                is_direct_factor = False
                ns = G.normal_subgroups()
                is_normal = any(M.order() == N.order() and M.is_subgroup(N) for N in ns)
                if is_normal:
                    for K in ns:
                        if M.order() * K.order() == G.order():
                            if M.intersection(K).order() == 1:
                                is_direct_factor = True
                                break
                neg_q = not is_direct_factor
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: M is not a direct factor of G"
]

N_HYP = 1
NEG_Q_INDEX = 1