import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: N is a subgroup of G",
    "¬Q: N is a normal subgroup of G is not equivalent to N being a union of conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    n_elements = None
    
    # H_1: N is a subgroup of G
    try:
        if isinstance(N, PermutationGroup):
            h1 = bool(N.is_subgroup(G))
            n_elements = set(N.elements)
        else:
            n_elements = set(N)
            h1 = True
            if not n_elements:
                h1 = False
            elif not n_elements.issubset(set(G.elements)):
                h1 = False
            else:
                for a in n_elements:
                    if (a**-1) not in n_elements:
                        h1 = False
                        break
                    for b in n_elements:
                        if a * b not in n_elements:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # P: N is a normal subgroup of G
    try:
        if not h1:
            p = False
        elif isinstance(N, PermutationGroup):
            p = bool(N.is_normal(G))
        else:
            p = True
            for n in n_elements:
                for g in G.elements:
                    if g * n * (g**-1) not in n_elements:
                        p = False
                        break
                if not p:
                    break
    except Exception:
        p = False

    # Q: N is a union of conjugacy classes of G
    try:
        q = True
        if n_elements is None:
            q = False
        elif not n_elements.issubset(set(G.elements)):
            q = False
        else:
            for n in n_elements:
                for g in G.elements:
                    if g * n * (g**-1) not in n_elements:
                        q = False
                        break
                if not q:
                    break
    except Exception:
        q = False

    # ¬Q: The conclusion fails (P is not equivalent to Q)
    try:
        neg_q = bool(p != q)
    except Exception:
        neg_q = False

    return [h1, neg_q]