import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: M is a maximal subgroup of G",
    "H_2: The core of M in G is a solvable group",
    "¬Q: The core of M in G is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, M = witness
    except Exception:
        return [False, False, False]
        
    try:
        G_elements = list(G.generate_dimino())
        M_elements = list(M.generate_dimino())
        M_set = set(M_elements)
        G_set = set(G_elements)
    except Exception:
        return [False, False, False]

    # H1: M is a maximal subgroup of G
    try:
        if len(M_elements) >= len(G_elements):
            h1 = False
        else:
            is_sub = all(gen in G_set for gen in M.generators)
            if not is_sub:
                h1 = False
            else:
                h1 = True
                for g in G_elements:
                    if g not in M_set:
                        H = PermutationGroup(list(M.generators) + [g])
                        if H.order() != len(G_elements):
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H2: The core of M in G is a solvable group
    try:
        core_elements = []
        for x in M_elements:
            is_in_core = True
            for g in G_elements:
                if (~g * x * g) not in M_set:
                    is_in_core = False
                    break
            if is_in_core:
                core_elements.append(x)
                
        if len(core_elements) == 1:
            h2 = True
        else:
            core_group = PermutationGroup(core_elements)
            h2 = bool(core_group.is_solvable)
    except Exception:
        h2 = False

    # neg_Q: The core of M in G is NOT the trivial subgroup
    try:
        neg_q = len(core_elements) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]