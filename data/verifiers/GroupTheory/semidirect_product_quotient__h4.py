import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

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

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H3: H is a subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h3 = False

    # H4: N \cap H = {e}
    try:
        intersection_size = sum(1 for g in H.generate() if g in N)
        h4 = (intersection_size == 1)
    except Exception:
        h4 = False

    # neg_Q: G/N is NOT isomorphic to H
    try:
        order_GN = G.order() // N.order()
        if order_GN != H.order():
            neg_q = True
        else:
            id_G = next(g for g in G.generate() if g.is_Identity)
            cosets = [id_G]
            for g in G.generate():
                found = False
                for c in cosets:
                    if (g * ~c) in N:
                        found = True
                        break
                if not found:
                    cosets.append(g)
            
            def get_coset_idx(x):
                for i, c in enumerate(cosets):
                    if (x * ~c) in N:
                        return i
                return -1
            
            table_GN = []
            for c1 in cosets:
                row = []
                for c2 in cosets:
                    row.append(get_coset_idx(c1 * c2))
                table_GN.append(row)
            
            id_H = next(h for h in H.generate() if h.is_Identity)
            H_elements = [id_H] + [h for h in H.generate() if h != id_H]
            table_H = []
            for h1 in H_elements:
                row = []
                for h2 in H_elements:
                    row.append(H_elements.index(h1 * h2))
                table_H.append(row)
            
            orders_GN = []
            for c in cosets:
                for i in range(1, order_GN + 1):
                    if (c**i) in N:
                        orders_GN.append(i)
                        break
            orders_GN.sort()
            orders_H = sorted([h.order() for h in H_elements])
            
            if orders_GN != orders_H:
                neg_q = True
            else:
                if order_GN <= 7:
                    is_iso = False
                    for p in itertools.permutations(range(order_GN)):
                        if p[0] != 0:
                            continue
                        valid = True
                        for i in range(order_GN):
                            for j in range(order_GN):
                                if table_GN[p[i]][p[j]] != p[table_H[i][j]]:
                                    valid = False
                                    break
                            if not valid:
                                break
                        if valid:
                            is_iso = True
                            break
                    neg_q = not is_iso
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G/N is not isomorphic to H"
]

N_HYP = 4
NEG_Q_INDEX = 4