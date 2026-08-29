import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation

# Top-level setup
S1 = SymmetricGroup(1)
S2 = SymmetricGroup(2)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
trivial = CyclicGroup(1)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)

CONDITION_LABELS = [
    "H_1: G is the symmetric group S_p on p letters",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The order of the normalizer N_G(P) is not exactly p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, P = witness
        elif isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            if G is None or p is None or P is None:
                return [False, False, False]
        else:
            return [False, False, False]
        
        p = int(p)
    except Exception:
        return [False, False, False]

    # H_1: G is the symmetric group S_p on p letters
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            Sp = SymmetricGroup(p)
            try:
                h1 = G.is_isomorphic(Sp)
            except Exception:
                h1 = (G.order() == math.factorial(p)) and (G.degree <= p)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h2 = False
        else:
            is_sub = True
            try:
                is_sub = P.is_subgroup(G)
            except Exception:
                for gen in P.generators:
                    if gen not in G:
                        is_sub = False
                        break
            
            if not is_sub:
                h2 = False
            else:
                if p < 1:
                    h2 = False
                elif p == 1:
                    h2 = (P.order() == 1)
                else:
                    order_G = G.order()
                    max_power = 1
                    while order_G % (max_power * p) == 0:
                        max_power *= p
                    h2 = (P.order() == max_power)
    except Exception:
        h2 = False

    # neg_Q: The order of the normalizer N_G(P) is not exactly p(p-1)
    try:
        norm_order = -1
        if G.order() <= 5040:
            count = 0
            gens = P.generators
            for g in G.generate():
                is_norm = True
                for gen in gens:
                    if (~g * gen * g) not in P:
                        is_norm = False
                        break
                if is_norm:
                    count += 1
            norm_order = count
            
        if norm_order == -1:
            neg_q = False
        else:
            neg_q = (norm_order != p * (p - 1))
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]