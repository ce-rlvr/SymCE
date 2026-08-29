import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Checks the remaining hypotheses and the negated conclusion for the false conjecture:
    'If G is a finite group, p is a prime, and Q is a Sylow p-subgroup of G, 
    then there exists an element g in G such that gPg^{-1} = Q.'
    (The hypothesis 'P is a Sylow p-subgroup of G' was dropped).
    
    Expected witness format: (G, p, P, Q)
    """
    try:
        G, p, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: Q is a Sylow p-subgroup of G
    try:
        h3 = False
        if isinstance(Q, PermutationGroup) and p > 1:
            is_sub = True
            for gen in Q.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            if is_sub:
                n = G.order()
                k = 0
                while n % p == 0:
                    k += 1
                    n //= p
                if Q.order() == p**k:
                    h3 = True
    except Exception:
        h3 = False
        
    # ¬Q: There is NO element g in G such that gPg^{-1} = Q
    try:
        neg_q = False
        if isinstance(P, PermutationGroup):
            # Ensure P is a valid subgroup of G first
            is_sub = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            
            if is_sub:
                neg_q = True  # Assume no such g exists until we find one
                
                # If orders don't match, they cannot be conjugate.
                # If they do match, we search for a conjugating element.
                if P.order() == Q.order():
                    for g in G.generate():
                        conj_gens = [g * x * ~g for x in P.generators]
                        
                        if not conj_gens:
                            is_eq = (Q.order() == 1)
                        else:
                            H = PermutationGroup(conj_gens)
                            is_eq = True
                            # Since H and Q have the same order, H is a subgroup of Q iff H == Q
                            for gen in H.generators:
                                if not Q.contains(gen):
                                    is_eq = False
                                    break
                                    
                        if is_eq:
                            neg_q = False  # Found a conjugating element, so conclusion holds (neg_Q is False)
                            break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: Q is a Sylow p-subgroup of G",
    "¬Q: There is no element g in G such that gPg^{-1} = Q"
]

N_HYP = 3
NEG_Q_INDEX = 3