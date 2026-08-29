import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

# Top-level setup for potential witness expressions
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

def count_sylow(K, p):
    """Helper to count the number of Sylow p-subgroups of a finite group K."""
    S = K.sylow_subgroup(p)
    S_elements = list(S.generate())
    sylows = set()
    for g in K.generate():
        # Conjugate the Sylow subgroup S by g
        conj = frozenset(~g * s * g for s in S_elements)
        sylows.add(conj)
    return len(sylows)

def conditions(witness) -> list[bool]:
    try:
        G, p, H, P = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: H is a subgroup of G that contains P
    try:
        h3 = False
        if isinstance(H, PermutationGroup) and isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup):
            H_in_G = all(G.contains(g) for g in H.generators)
            P_in_H = all(H.contains(g) for g in P.generators)
            h3 = bool(H_in_G and P_in_H)
    except Exception:
        h3 = False
        
    # neg_Q: The conclusion fails
    # Conclusion: P is a Sylow p-subgroup of H, and n_p(H) divides n_p(G)
    try:
        if not (isinstance(H, PermutationGroup) and isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup)):
            neg_q = False
        else:
            # Check if P is a Sylow p-subgroup of H
            order_H = H.order()
            k = 0
            while order_H % p == 0:
                order_H //= p
                k += 1
                
            P_in_H = all(H.contains(g) for g in P.generators)
            is_sylow_in_H = (P.order() == p**k) and P_in_H
            
            if not is_sylow_in_H:
                q = False
            else:
                # Check if n_p(H) divides n_p(G)
                n_H = count_sylow(H, p)
                n_G = count_sylow(G, p)
                q = (n_G % n_H == 0)
                
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: H is a subgroup of G that contains P",
    "¬Q: P is not a Sylow p-subgroup of H, or the number of Sylow p-subgroups of H does not divide the number of Sylow p-subgroups of G"
]

N_HYP = 3
NEG_Q_INDEX = 3