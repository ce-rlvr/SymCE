import math
from itertools import combinations
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
V4 = Z2 * Z2

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h2 = False
        else:
            p_val = int(p)
            if p_val <= 1:
                h2 = False
            else:
                G_elems = set(G.generate())
                P_elems = set(P.generate())
                is_sub = P_elems.issubset(G_elems)
                
                order_G = G.order()
                order_P = P.order()
                
                k = 0
                temp = order_G
                while temp % p_val == 0:
                    k += 1
                    temp //= p_val
                
                expected_order = p_val**k
                h2 = is_sub and (order_P == expected_order)
    except Exception:
        h2 = False
        
    # neg_Q: P is a normal subgroup of G if and only if P is the unique Sylow p-subgroup of G (must fail)
    try:
        if not h2:
            expected_order = P.order() if isinstance(P, PermutationGroup) else 1
            G_elems = set(G.generate()) if isinstance(G, PermutationGroup) else set()
            P_elems = set(P.generate()) if isinstance(P, PermutationGroup) else set()
            
        # Check normality
        is_normal = True
        for g in G_elems:
            g_inv = ~g
            for h in P_elems:
                conj = g * h * g_inv
                if conj not in P_elems:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        # Check uniqueness
        G_order = G.order() if isinstance(G, PermutationGroup) else -1
        if expected_order == G_order:
            is_unique = True
        else:
            elements = [g for g in G_elems if expected_order % g.order() == 0]
            
            if h2:
                P_elems_frozen = frozenset(P.generate())
            else:
                P_elems_frozen = frozenset(P_elems)
                
            subgroups = {P_elems_frozen}
            max_gens = int(math.log2(expected_order)) + 1 if expected_order > 0 else 1
            
            for r in range(1, max_gens + 1):
                for gens in combinations(elements, r):
                    # Optimization: if all generators are already in P, they generate a subgroup of P.
                    # Since we are looking for subgroups of the same order as P, it can only be P itself.
                    if all(g in P_elems_frozen for g in gens):
                        continue
                    try:
                        H = PermutationGroup(list(gens))
                        if H.order() == expected_order:
                            subgroups.add(frozenset(H.generate()))
                            if len(subgroups) > 1:
                                break
                    except Exception:
                        pass
                if len(subgroups) > 1:
                    break
            
            is_unique = (len(subgroups) == 1)
        
        Q = (is_normal == is_unique)
        neg_q = not Q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: P is normal but not unique, or unique but not normal"
]

N_HYP = 2
NEG_Q_INDEX = 2