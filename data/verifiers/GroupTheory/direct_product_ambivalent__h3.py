import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for witness expressions
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

def is_ambivalent(grp):
    """
    A group is ambivalent if every element is conjugate to its inverse.
    """
    try:
        elements = list(grp.elements)
        for g in elements:
            g_inv = ~g
            if g == g_inv:
                continue
            # Check if g_inv is in the conjugacy class of g
            if not any(x * g * ~x == g_inv for x in elements):
                return False
        return True
    except Exception:
        return False

def direct_product(G, H):
    """
    Constructs the direct product of two permutation groups.
    """
    try:
        # SymPy's PermutationGroup multiplication is the direct product
        res = G * H
        if isinstance(res, PermutationGroup):
            return res
    except Exception:
        pass
    
    # Fallback manual construction
    gens = []
    size_G = G.degree
    size_H = H.degree
    for g in G.generators:
        a = list(g.array_form)
        if len(a) < size_G:
            a += list(range(len(a), size_G))
        a += list(range(size_G, size_G + size_H))
        gens.append(Permutation(a))
    for h in H.generators:
        a = list(range(size_G))
        b = list(h.array_form)
        if len(b) < size_H:
            b += list(range(len(b), size_H))
        a += [x + size_G for x in b]
        gens.append(Permutation(a))
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: G is an ambivalent group
    try:
        h2_ok = is_ambivalent(G)
    except Exception:
        h2_ok = False
        
    # ¬Q: The direct product G \times H is NOT an ambivalent group
    try:
        if h1_ok:
            GxH = direct_product(G, H)
            neg_q_ok = not is_ambivalent(GxH)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is an ambivalent group",
    "¬Q: G x H is not an ambivalent group"
]

N_HYP = 2
NEG_Q_INDEX = 2