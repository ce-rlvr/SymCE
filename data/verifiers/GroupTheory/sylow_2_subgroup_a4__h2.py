import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup

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

def get_order(obj):
    try:
        return obj.order()
    except TypeError:
        return obj.order

def group_contains(group, elem):
    try:
        return group.contains(elem)
    except Exception:
        return elem in group

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
        else:
            G = A4
            P = witness
            
        h1 = False
        if hasattr(G, 'is_isomorphic') and hasattr(P, 'generators'):
            if G == A4 or G.is_isomorphic(A4):
                if all(group_contains(G, g) for g in P.generators):
                    h1 = True
    except Exception:
        h1 = False

    try:
        if not hasattr(P, 'generators') or not hasattr(G, 'generators'):
            neg_q = False
        else:
            is_subgroup_PG = all(group_contains(G, g) for g in P.generators)
            
            is_normal = is_subgroup_PG
            if is_normal:
                for g in G.generators:
                    for h in P.generators:
                        if not group_contains(P, ~g * h * g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            is_v4 = False
            p_order = get_order(P)
            if p_order == 4:
                is_v4 = all(get_order(g) <= 2 for g in P.generators)
                
            q = is_normal and is_v4
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the alternating group A_4 of degree 4",
    "¬Q: P is not a normal subgroup of G isomorphic to V_4"
]

N_HYP = 1
NEG_Q_INDEX = 1