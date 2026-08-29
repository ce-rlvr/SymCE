import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
D6 = DihedralGroup(6)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, P, p = witness
            elif len(witness) == 2:
                G, P = witness
                p = P.order()
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: P is a Sylow p-subgroup of G
    try:
        if not isinstance(p, int) or p <= 1:
            h1 = False
        elif not P.is_subgroup(G):
            h1 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            while order_G % (p**(k+1)) == 0:
                k += 1
            h1 = (order_P == p**k)
    except Exception:
        h1 = False

    # neg_Q: P is NOT the unique Sylow p-subgroup of N_G(P)
    try:
        if not isinstance(p, int) or p <= 1:
            neg_q = False
        else:
            # Find N_G(P)
            n_gens = []
            P_gens = P.generators
            for g in G.elements:
                if all(P.contains(g * h * ~g) for h in P_gens):
                    n_gens.append(g)
            
            N = PermutationGroup(n_gens)
            
            order_N = N.order()
            m = 0
            while order_N % (p**(m+1)) == 0:
                m += 1
            target_order = p**m
            
            elements = list(N.elements)
            elements_not_in_P = [g for g in elements if not P.contains(g)]
            
            is_unique = True
            
            # 1-generated subgroups
            for g in elements_not_in_P:
                H = PermutationGroup([g])
                if H.order() == target_order:
                    is_unique = False
                    break
            
            # 2-generated subgroups
            if is_unique:
                for g1 in elements_not_in_P:
                    for g2 in elements:
                        H = PermutationGroup([g1, g2])
                        if H.order() == target_order and not H.is_subgroup(P):
                            is_unique = False
                            break
                    if not is_unique:
                        break
                        
            # 3-generated subgroups
            if is_unique and target_order >= 8:
                for g1 in elements_not_in_P:
                    for j in range(len(elements)):
                        g2 = elements[j]
                        for k_idx in range(j+1, len(elements)):
                            g3 = elements[k_idx]
                            H = PermutationGroup([g1, g2, g3])
                            if H.order() == target_order and not H.is_subgroup(P):
                                is_unique = False
                                break
                        if not is_unique:
                            break
                    if not is_unique:
                        break

            neg_q = not is_unique
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "¬Q: P is not the unique Sylow p-subgroup of N_G(P)"
]

N_HYP = 1
NEG_Q_INDEX = 1