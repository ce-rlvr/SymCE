import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([1, 0, 3, 2]), Permutation([2, 3, 0, 1])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_padded_array(p, deg):
    arr = p.array_form
    if len(arr) < deg:
        arr = arr + list(range(len(arr), deg))
    return arr

def direct_product(G, H):
    degG = G.degree
    degH = H.degree
    if degG == 0: degG = 1
    if degH == 0: degH = 1
    gens = []
    for g in G.generators:
        arr = get_padded_array(g, degG)
        arr += list(range(degG, degG + degH))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = list(range(degG))
        arr_h = get_padded_array(h, degH)
        arr += [x + degG for x in arr_h]
        gens.append(Permutation(arr))
    if not gens:
        return PermutationGroup([Permutation(list(range(degG + degH)))])
    return PermutationGroup(gens)

def is_rational_group(grp):
    try:
        elements = list(grp.elements)
    except Exception:
        elements = list(grp.generate())
    
    checked = set()
    for g in elements:
        if g in checked:
            continue
        ord_g = g.order()
        orbit = {x * g * ~x for x in elements}
        checked.update(orbit)
        for k in range(1, ord_g):
            if math.gcd(k, ord_g) == 1:
                if (g**k) not in orbit:
                    return False
    return True

def conditions(witness):
    try:
        G, H = witness
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = is_rational_group(H)
    except Exception:
        h2 = False

    try:
        GxH = direct_product(G, H)
        neg_q = not is_rational_group(GxH)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: H is a rational group",
    "¬Q: G x H is not a rational group"
]

N_HYP = 2
NEG_Q_INDEX = 2