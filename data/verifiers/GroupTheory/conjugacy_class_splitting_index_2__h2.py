import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        G, H, C = witness
    except Exception:
        return [False, False, False, False, False]
        
    try:
        try:
            C_set = set(C)
        except Exception:
            C_set = set(C.elements)
    except Exception:
        C_set = set()

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False

    # H2: The index of H in G is exactly 2
    try:
        order_G = G.order()
        if isinstance(H, PermutationGroup):
            try:
                is_sub = H.is_subgroup(G)
            except AttributeError:
                is_sub = set(H.elements).issubset(set(G.elements))
            
            if is_sub:
                order_H = H.order()
                h2 = (order_G == 2 * order_H)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: C is a conjugacy class of G
    try:
        c_classes = G.conjugacy_classes()
        h3 = False
        for cc in c_classes:
            try:
                cc_set = set(cc)
            except Exception:
                cc_set = set(cc.elements)
            if cc_set == C_set and len(C_set) > 0:
                h3 = True
                break
    except Exception:
        h3 = False

    # H4: C is a subset of H
    try:
        try:
            H_elements = set(H.elements)
        except AttributeError:
            H_elements = set(H)
            
        h4 = C_set.issubset(H_elements) and len(C_set) > 0
    except Exception:
        h4 = False

    # Conclusion: C is either a single conjugacy class in H, or C is the disjoint union of exactly two conjugacy classes of H of equal size.
    try:
        if not isinstance(H, PermutationGroup):
            q = False
        else:
            H_classes = H.conjugacy_classes()
            classes_in_C = []
            for hc in H_classes:
                try:
                    hc_set = set(hc)
                except Exception:
                    hc_set = set(hc.elements)
                
                if hc_set.issubset(C_set):
                    classes_in_C.append(hc_set)
            
            union_in_C = set()
            for hc_set in classes_in_C:
                union_in_C.update(hc_set)
                
            if union_in_C != C_set or len(C_set) == 0:
                q = False
            else:
                if len(classes_in_C) == 1:
                    q = True
                elif len(classes_in_C) == 2:
                    q = (len(classes_in_C[0]) == len(classes_in_C[1]))
                else:
                    q = False
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The index of H in G is exactly 2",
    "H_3: C is a conjugacy class of G",
    "H_4: C is a subset of H",
    "¬Q: C is not a single conjugacy class in H, nor the disjoint union of exactly two equal-sized classes"
]

N_HYP = 4
NEG_Q_INDEX = 4