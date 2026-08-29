import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup
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

def direct_product(G, H):
    degG = G.degree
    degH = H.degree
    if degG == 0 and degH == 0:
        return PermutationGroup([Permutation()])
    if degG == 0:
        return H
    if degH == 0:
        return G
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr.extend(list(range(len(arr), degG)))
        p = arr + list(range(degG, degG + degH))
        gens.append(Permutation(p))
    for h in H.generators:
        arr = list(h.array_form)
        if len(arr) < degH:
            arr.extend(list(range(len(arr), degH)))
        p = list(range(degG)) + [x + degG for x in arr]
        gens.append(Permutation(p))
    return PermutationGroup(gens)

def is_ambivalent(grp):
    if not isinstance(grp, PermutationGroup):
        return False
    elements = list(grp.generate())
    for x in elements:
        x_inv = ~x
        if x == x_inv:
            continue
        found = False
        for y in elements:
            if y * x * ~y == x_inv:
                found = True
                break
        if not found:
            return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: H is an ambivalent group
    try:
        h2_ok = is_ambivalent(H)
    except Exception:
        h2_ok = False
        
    # neg_Q: G \times H is NOT an ambivalent group
    try:
        if not h1_ok:
            neg_q = False
        else:
            GxH = direct_product(G, H)
            neg_q = not is_ambivalent(GxH)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is an ambivalent group",
    "¬Q: G \\times H is not an ambivalent group"
]

N_HYP = 2
NEG_Q_INDEX = 2