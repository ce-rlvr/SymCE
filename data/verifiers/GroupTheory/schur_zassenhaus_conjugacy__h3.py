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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: H_1 and H_2 are two complements of N in G",
    "¬Q: H_1 and H_2 are not conjugate subgroups in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False] * 4
        G, N, H1, H2 = witness
    except Exception:
        return [False] * 4

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            is_sub_N = all(G.contains(n) for n in N.generators)
            if is_sub_N:
                is_normal = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if not N.contains(g * n * g_inv):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2_ok = is_normal
    except Exception:
        h2_ok = False

    # H_3: H_1 and H_2 are two complements of N in G
    try:
        h3_ok = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and \
           isinstance(H1, PermutationGroup) and isinstance(H2, PermutationGroup):
            is_sub_H1 = all(G.contains(h) for h in H1.generators)
            is_sub_H2 = all(G.contains(h) for h in H2.generators)
            if is_sub_H1 and is_sub_H2:
                if N.order() * H1.order() == G.order() and N.order() * H2.order() == G.order():
                    int1_trivial = all(h.is_Identity or not N.contains(h) for h in H1.generate())
                    int2_trivial = all(h.is_Identity or not N.contains(h) for h in H2.generate())
                    if int1_trivial and int2_trivial:
                        h3_ok = True
    except Exception:
        h3_ok = False

    # ¬Q: H_1 and H_2 are not conjugate subgroups in G
    try:
        neg_q_ok = False
        if isinstance(G, PermutationGroup) and isinstance(H1, PermutationGroup) and isinstance(H2, PermutationGroup):
            if H1.order() == H2.order():
                are_conjugate = False
                for g in G.generate():
                    g_inv = ~g
                    maps_into = True
                    for h in H1.generators:
                        try:
                            conj = g * h * g_inv
                        except Exception:
                            maps_into = False
                            break
                        if not H2.contains(conj):
                            maps_into = False
                            break
                    if maps_into:
                        are_conjugate = True
                        break
                neg_q_ok = not are_conjugate
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]