import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, H, f, A, B = witness
    except Exception:
        return [False] * 5

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: f is a surjective group homomorphism from G to H
    try:
        G_elements = list(G.generate())
        if callable(f):
            f_dict = {g: f(g) for g in G_elements}
        else:
            f_dict = f
    except Exception:
        f_dict = None

    try:
        H_elements = list(H.generate())
        if f_dict is None or not all(g in f_dict for g in G_elements):
            h2 = False
        else:
            is_hom = True
            for x in G_elements:
                for y in G_elements:
                    if f_dict[x * y] != f_dict[x] * f_dict[y]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            if is_hom:
                image = set(f_dict[g] for g in G_elements)
                h2 = (image == set(H_elements))
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: A and B are subgroups of G
    try:
        h3 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and A.is_subgroup(G) and B.is_subgroup(G)
    except Exception:
        h3 = False

    # H_4: A is a subgroup of B
    try:
        h4 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and A.is_subgroup(B)
    except Exception:
        h4 = False

    # neg_Q: index of A in B != index of f(A) in f(B)
    try:
        B_order = B.order()
        A_order = A.order()
        
        fB_elements = set(f_dict[x] for x in B.generate())
        fA_elements = set(f_dict[x] for x in A.generate())
        
        # Using cross-multiplication to avoid floating point comparisons
        # index of A in B = B_order / A_order
        # index of f(A) in f(B) = len(fB_elements) / len(fA_elements)
        neg_q = (B_order * len(fA_elements) != A_order * len(fB_elements))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism from G to H",
    "H_3: A and B are subgroups of G",
    "H_4: A is a subgroup of B",
    "¬Q: The index of A in B is not equal to the index of f(A) in f(B)"
]

N_HYP = 4
NEG_Q_INDEX = 4