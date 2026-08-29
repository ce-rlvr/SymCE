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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: G is a cyclic group of order m",
    "H_3: H is a cyclic group of order n",
    "¬Q: The direct product G x H is not a cyclic group of order mn"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_cyclic_group(G):
    """Check if a permutation group is cyclic."""
    try:
        order = G.order()
        if order > 2000:
            return False
        
        # Check if any generator has the full order
        for g in G.generators:
            if g.order() == order:
                return True
                
        # Otherwise check all elements
        elements = G.elements if hasattr(G, 'elements') else G.generate()
        for g in elements:
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def direct_product(G, H):
    """Construct the external direct product of two permutation groups."""
    size_G = G.degree
    size_H = H.degree
    
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < size_G:
            arr += list(range(len(arr), size_G))
        arr += [size_G + i for i in range(size_H)]
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(size_G))
        h_arr = list(h.array_form)
        if len(h_arr) < size_H:
            h_arr += list(range(len(h_arr), size_H))
        arr += [size_G + i for i in h_arr]
        gens.append(Permutation(arr))
    
    if not gens:
        size = max(1, size_G + size_H)
        return PermutationGroup([Permutation(size - 1)])
    return PermutationGroup(gens)

def conditions(witness):
    m, n, G, H = None, None, None, None
    
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                try:
                    is_num = (int(witness[0]) == witness[0]) and (int(witness[1]) == witness[1])
                except Exception:
                    is_num = False
                
                if is_num:
                    m, n = witness
                    if m > 0:
                        G = CyclicGroup(int(m))
                    if n > 0:
                        H = CyclicGroup(int(n))
                else:
                    G, H = witness
                    m = G.order()
                    n = H.order()
            elif len(witness) == 4:
                m, n, G, H = witness
    except Exception:
        pass

    # H_1: m and n are positive integers
    try:
        h1 = (int(m) == m) and (int(n) == n) and (m > 0) and (n > 0)
    except Exception:
        h1 = False

    # H_2: G is a cyclic group of order m
    try:
        h2 = is_cyclic_group(G) and G.order() == m
    except Exception:
        h2 = False

    # H_3: H is a cyclic group of order n
    try:
        h3 = is_cyclic_group(H) and H.order() == n
    except Exception:
        h3 = False

    # ¬Q: The direct product G x H is not a cyclic group of order mn
    try:
        GxH = direct_product(G, H)
        is_cyclic = is_cyclic_group(GxH)
        is_order_mn = (GxH.order() == m * n)
        neg_q = not (is_cyclic and is_order_mn)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]