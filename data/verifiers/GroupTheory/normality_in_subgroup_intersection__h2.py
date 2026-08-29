import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(G.contains(g) for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: N \cap H is not a normal subgroup of H
    try:
        if isinstance(H, PermutationGroup):
            elements_H = set(H.generate())
        else:
            elements_H = set()

        if isinstance(N, PermutationGroup):
            elements_N = set(N.generate())
        else:
            try:
                elements_N = set(N)
            except Exception:
                elements_N = set()

        intersection = elements_H.intersection(elements_N)

        is_normal_subgroup = True
        if not intersection:
            is_normal_subgroup = False
        else:
            # Find identity in H
            identity = None
            for h in elements_H:
                if h * h == h:
                    identity = h
                    break
            
            if identity is None or identity not in intersection:
                is_normal_subgroup = False
            else:
                # Check closure under multiplication
                for a in intersection:
                    for b in intersection:
                        if a * b not in intersection:
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
                
                # Check closure under inverses
                if is_normal_subgroup:
                    for a in intersection:
                        if ~a not in intersection:
                            is_normal_subgroup = False
                            break
                
                # Check normality in H
                if is_normal_subgroup:
                    for h in elements_H:
                        for n in intersection:
                            # Conjugation: h * n * h^-1
                            if h * n * ~h not in intersection:
                                is_normal_subgroup = False
                                break
                        if not is_normal_subgroup:
                            break

        neg_q = not is_normal_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: N \\cap H is not a normal subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2