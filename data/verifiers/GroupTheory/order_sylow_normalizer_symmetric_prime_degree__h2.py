import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

# Top-level setup: named object bindings for witness expressions
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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The order of the normalizer N_G(P) is not exactly p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        if not (hasattr(G, 'generators') and hasattr(P, 'generators')):
            h2 = False
        else:
            # Check if P is a subgroup of G
            is_subgroup = all(G.contains(x) for x in P.generators)
            if not is_subgroup:
                h2 = False
            else:
                order_G = G.order()
                order_P = P.order()
                
                # Calculate the highest power of p dividing the order of G
                k = 0
                temp = order_G
                while temp % p == 0 and temp > 0:
                    k += 1
                    temp //= p
                
                expected_order = p**k
                h2 = bool(order_P == expected_order)
    except Exception:
        h2 = False
        
    # neg_Q: The order of the normalizer N_G(P) is not exactly p(p-1)
    try:
        count = 0
        P_gens = P.generators
        # Iterate over all elements in G to find those that normalize P
        for g in G.generate():
            normalizes = True
            for x in P_gens:
                # Conjugate x by g
                conj = g * x * (~g)
                if not P.contains(conj):
                    normalizes = False
                    break
            if normalizes:
                count += 1
        
        neg_q = bool(count != p * (p - 1))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]