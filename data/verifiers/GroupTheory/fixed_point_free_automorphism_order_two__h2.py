import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]

    def apply_phi(x):
        if isinstance(phi, dict):
            return phi.get(x, None)
        else:
            return phi(x)

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = list(G.generate())
            elem_set = set(elements)
        else:
            elements = []
            elem_set = set()
    except Exception:
        h1 = False
        elements = []
        elem_set = set()

    # H2: \phi(\phi(x)) = x for all x \in G
    try:
        if not h1 or not elements:
            h2 = False
        else:
            h2 = True
            for x in elements:
                px = apply_phi(x)
                if px not in elem_set:
                    h2 = False
                    break
                if apply_phi(px) != x:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: \phi(x) = x implies x = e
    try:
        if not h1 or not elements:
            h3 = False
        else:
            h3 = True
            e = G.identity
            for x in elements:
                if apply_phi(x) == x:
                    if x != e:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # ¬Q: G is not abelian or \phi(x) != x^{-1} for some x \in G
    try:
        if not h1 or not elements:
            neg_q = False
        else:
            is_abelian = G.is_abelian
            phi_is_inv = True
            for x in elements:
                px = apply_phi(x)
                if px != x**-1:
                    phi_is_inv = False
                    break
            neg_q = not (is_abelian and phi_is_inv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \\phi(\\phi(x)) = x for all x \\in G",
    "H_3: \\phi(x) = x implies x = e",
    "¬Q: G is not abelian or \\phi(x) != x^{-1} for some x \\in G"
]

N_HYP = 3
NEG_Q_INDEX = 3