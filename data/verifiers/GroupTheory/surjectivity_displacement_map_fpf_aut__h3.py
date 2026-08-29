import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    try:
        elements = list(G.elements)
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        else:
            phi_func = phi

        h2 = True
        images = set()
        for g in elements:
            img = phi_func(g)
            if img not in elements:
                h2 = False
                break
            images.add(img)

        if h2 and len(images) != len(elements):
            h2 = False

        if h2:
            for x in elements:
                for y in elements:
                    if phi_func(x * y) != phi_func(x) * phi_func(y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    try:
        elements = list(G.elements)
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        else:
            phi_func = phi

        f_images = set()
        for x in elements:
            val = (x**-1) * phi_func(x)
            f_images.add(val)

        neg_q = len(f_images) < len(elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: phi is an automorphism of G",
    "¬Q: The map f(x) = x^{-1}phi(x) is not a bijection"
]

N_HYP = 2
NEG_Q_INDEX = 2