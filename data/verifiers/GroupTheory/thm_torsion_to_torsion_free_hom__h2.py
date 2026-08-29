import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a torsion group
    try:
        g_elements = list(G.generate())
        h1 = isinstance(G, PermutationGroup)
        if h1:
            for g in g_elements:
                if g.order() <= 0:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    mapping = {}
    try:
        h2 = True
        h_elements = list(H.generate())
        if isinstance(phi, dict):
            mapping = phi
        elif callable(phi):
            mapping = {g: phi(g) for g in g_elements}
        else:
            h2 = False
            
        if h2:
            if set(mapping.keys()) != set(g_elements):
                h2 = False
            elif not all(v in h_elements for v in mapping.values()):
                h2 = False
            else:
                for x in g_elements:
                    for y in g_elements:
                        if mapping[x * y] != mapping[x] * mapping[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: phi is not the trivial homomorphism
    try:
        neg_q = False
        if h2:
            id_H = None
            for h in h_elements:
                if h * h == h:
                    id_H = h
                    break
            for x in g_elements:
                if mapping[x] != id_H:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a torsion group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2