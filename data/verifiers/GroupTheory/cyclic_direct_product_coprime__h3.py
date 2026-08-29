import math
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_cyclic(grp):
    if not isinstance(grp, PermutationGroup):
        return False
    order = grp.order()
    if order > 2000:
        return False
    for g in grp.elements:
        if g.order() == order:
            return True
    return False

def conditions(witness):
    try:
        m, n, G, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: m and n are positive integers
    try:
        m_val = int(m)
        n_val = int(n)
        h1 = (m_val == m) and (n_val == n) and (m_val > 0) and (n_val > 0)
    except Exception:
        h1 = False

    # H2: G is a cyclic group of order m
    try:
        h2 = isinstance(G, PermutationGroup) and G.order() == m_val and is_cyclic(G)
    except Exception:
        h2 = False

    # H3: gcd(m, n) = 1
    try:
        h3 = math.gcd(m_val, n_val) == 1
    except Exception:
        h3 = False

    # ¬Q: The direct product G x H is NOT a cyclic group of order mn
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            try:
                GxH = G * H
            except Exception:
                deg_G = G.degree
                deg_H = H.degree
                gens = []
                for g in G.generators:
                    arr = g.array_form
                    if len(arr) < deg_G:
                        arr = arr + list(range(len(arr), deg_G))
                    gens.append(Permutation(arr + list(range(deg_G, deg_G + deg_H))))
                for h in H.generators:
                    arr = h.array_form
                    if len(arr) < deg_H:
                        arr = arr + list(range(len(arr), deg_H))
                    gens.append(Permutation(list(range(deg_G)) + [x + deg_G for x in arr]))
                if not gens:
                    GxH = PermutationGroup(Permutation())
                else:
                    GxH = PermutationGroup(gens)
            
            if GxH.order() != m_val * n_val:
                neg_q = True
            else:
                neg_q = not is_cyclic(GxH)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: G is a cyclic group of order m",
    "H_3: gcd(m, n) = 1",
    "¬Q: G x H is not a cyclic group of order mn"
]

N_HYP = 3
NEG_Q_INDEX = 3