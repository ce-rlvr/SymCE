import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, f = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f: G -> G is a group homomorphism
    try:
        h2 = True
        elements = list(G.elements)
        for x in elements:
            val_x = f(x) if callable(f) else f[x]
            if val_x not in elements:
                h2 = False
                break
            for y in elements:
                val_y = f(y) if callable(f) else f[y]
                val_xy = f(x*y) if callable(f) else f[x*y]
                if val_xy != val_x * val_y:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # neg_Q: f is not an automorphism of G
    try:
        elements = list(G.elements)
        is_hom = True
        image = set()
        for x in elements:
            val_x = f(x) if callable(f) else f[x]
            if val_x not in elements:
                is_hom = False
                break
            image.add(val_x)
            for y in elements:
                val_y = f(y) if callable(f) else f[y]
                val_xy = f(x*y) if callable(f) else f[x*y]
                if val_xy != val_x * val_y:
                    is_hom = False
                    break
            if not is_hom:
                break
        
        is_bij = len(image) == len(elements)
        is_auto = is_hom and is_bij
        neg_q = not is_auto
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: f: G -> G is a group homomorphism",
    "¬Q: f is not an automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2