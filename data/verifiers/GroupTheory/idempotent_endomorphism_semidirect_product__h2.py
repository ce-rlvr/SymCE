import itertools
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    try:
        G, f = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'identity')
        if h1:
            elements = list(G.elements)
            e = G.identity
    except Exception:
        h1 = False

    try:
        h2 = True
        for x in elements:
            if f[f[x]] != f[x]:
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        ker = {x for x in elements if f[x] == e}
        im = {f[x] for x in elements}

        is_semidirect = True

        if e not in ker:
            is_semidirect = False
        else:
            for x in ker:
                if x**-1 not in ker:
                    is_semidirect = False
                    break
                for y in ker:
                    if x * y not in ker:
                        is_semidirect = False
                        break
                for g in elements:
                    if g * x * g**-1 not in ker:
                        is_semidirect = False
                        break

        if is_semidirect:
            if e not in im:
                is_semidirect = False
            else:
                for x in im:
                    if x**-1 not in im:
                        is_semidirect = False
                        break
                    for y in im:
                        if x * y not in im:
                            is_semidirect = False
                            break

        if is_semidirect:
            if ker.intersection(im) != {e}:
                is_semidirect = False

        if is_semidirect:
            prod = {n * h for n in ker for h in im}
            if prod != set(elements):
                is_semidirect = False

        neg_q = not is_semidirect

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: f o f = f",
    "¬Q: G is not the internal semidirect product of ker(f) and im(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2