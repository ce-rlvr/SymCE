import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import math

# Top-level setup
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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The order of H is n
    try:
        n = H.order()
        h2_ok = isinstance(H, PermutationGroup) and n > 0
    except Exception:
        h2_ok = False

    # H_3: There is no other subgroup of G of order n besides H
    try:
        if not (h1_ok and h2_ok):
            h3_ok = False
        else:
            elements = list(G.generate())
            if n > len(elements) or len(elements) % n != 0:
                subgroups_of_order_n = []
            else:
                subgroups_of_order_n = []
                id_el = G.identity
                elements_without_id = [e for e in elements if e != id_el]
                
                for subset_without_id in itertools.combinations(elements_without_id, n - 1):
                    subset_set = set(subset_without_id)
                    subset_set.add(id_el)
                    
                    # Quick inverse check
                    is_subgroup = True
                    for a in subset_without_id:
                        if (~a) not in subset_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        continue
                        
                    # Full closure check
                    for a in subset_without_id:
                        for b in subset_without_id:
                            if (a * b) not in subset_set:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                            
                    if is_subgroup:
                        subgroups_of_order_n.append(subset_set)
            
            H_elements = set(H.generate())
            h3_ok = True
            for K_elements in subgroups_of_order_n:
                if K_elements != H_elements:
                    h3_ok = False
                    break
    except Exception:
        h3_ok = False

    # ¬Q: H is not a normal subgroup of G
    try:
        if not (h1_ok and h2_ok):
            neg_Q = False
        else:
            H_elements = set(H.generate())
            G_elements = set(G.generate())
            is_subgroup = H_elements.issubset(G_elements)
            
            if not is_subgroup:
                is_normal = False
            else:
                is_normal = True
                for g in G_elements:
                    for h in H_elements:
                        if (g * h * ~g) not in H_elements:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            neg_Q = not is_normal
    except Exception:
        neg_Q = False

    return [h1_ok, h2_ok, h3_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of H is n",
    "H_3: There is no other subgroup of G of order n besides H",
    "¬Q: H is not a normal subgroup of G"
]
N_HYP = 3
NEG_Q_INDEX = 3