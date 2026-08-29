import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, S_list = witness
        else:
            G = witness
            S_list = None
    except Exception:
        return [False, False, False]

    # H_1: Let G be a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: Let G = S_1 \times S_2 \times \dots \times S_k be a decomposition of G into a direct product of non-abelian simple groups S_i
    try:
        h2_ok = True
        if not isinstance(S_list, (list, tuple)):
            h2_ok = False
        else:
            for S in S_list:
                if not isinstance(S, PermutationGroup):
                    h2_ok = False
                    break
                if S.is_abelian:
                    h2_ok = False
                    break
                # Check if S is simple (composition series length is exactly 2: the group itself and the trivial group)
                if len(S.composition_series()) != 2:
                    h2_ok = False
                    break
            
            if h2_ok:
                # Check if G is the internal direct product of S_list
                is_internal = True
                for S in S_list:
                    for gen in S.generators:
                        if gen not in G:
                            is_internal = False
                            break
                    if not is_internal: break
                
                if is_internal:
                    # Check that elements from different factors commute
                    for i in range(len(S_list)):
                        for j in range(i + 1, len(S_list)):
                            for g1 in S_list[i].generators:
                                for g2 in S_list[j].generators:
                                    if g1 * g2 != g2 * g1:
                                        is_internal = False
                                        break
                                if not is_internal: break
                        if not is_internal: break
                    
                    # Check that the orders multiply correctly
                    if is_internal:
                        prod_order = 1
                        for S in S_list:
                            prod_order *= S.order()
                        if G.order() != prod_order:
                            is_internal = False
                
                if not is_internal:
                    # Check if G is isomorphic to the external direct product
                    if len(S_list) == 0:
                        if G.order() != 1:
                            h2_ok = False
                    else:
                        DP = S_list[0]
                        for S in S_list[1:]:
                            DP = DP * S
                        if not G.is_isomorphic(DP):
                            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The composition length of G is NOT exactly k, OR the multiset of composition factors is NOT exactly {S_1, ..., S_k}
    try:
        if not isinstance(S_list, (list, tuple)):
            neg_q_ok = False
        else:
            k = len(S_list)
            comp_series = G.composition_series()
            comp_length = len(comp_series) - 1
            
            if comp_length != k:
                neg_q_ok = True
            else:
                # Calculate the orders of the composition factors
                factor_orders = []
                for i in range(len(comp_series) - 1):
                    factor_orders.append(comp_series[i].order() // comp_series[i+1].order())
                
                s_orders = [S.order() for S in S_list]
                
                # Since simple groups of the same order are isomorphic for small orders,
                # comparing the multiset of orders is sufficient to check isomorphism classes.
                if sorted(factor_orders) != sorted(s_orders):
                    neg_q_ok = True
                else:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a direct product of non-abelian simple groups S_i",
    "¬Q: The composition length of G is not k, or the multiset of composition factors is not exactly {S_1, ..., S_k}"
]

N_HYP = 2
NEG_Q_INDEX = 2