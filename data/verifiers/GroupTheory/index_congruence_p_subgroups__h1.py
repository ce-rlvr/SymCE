import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint
from sympy import oo

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Given a witness (G, H, p), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: H is a p-subgroup of G
    try:
        order = H.order()
        
        # Check if H is a subgroup of G
        if order == 1:
            is_sub = True
        elif hasattr(H, 'is_subgroup') and hasattr(G, 'is_subgroup'):
            is_sub = H.is_subgroup(G)
        else:
            is_sub = all(g in G for g in H.generators)
            
        if not is_sub:
            h2 = False
        else:
            # Check if H is a p-group (order is a power of p)
            if order == 1:
                h2 = True
            elif order == oo:
                h2 = False
            else:
                f = factorint(order)
                h2 = (list(f.keys()) == [p])
    except Exception:
        h2 = False
        
    # neg_Q: index of H in G is not congruent to index of H in N_G(H) mod p
    try:
        # Determine elements of G to compute the normalizer
        if hasattr(G, 'generate_dimino'):
            elements = list(G.generate_dimino())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = None
            
        if elements is not None:
            n_order = 0
            h_gens = H.generators
            
            # Compute the order of the normalizer N_G(H)
            for g in elements:
                # g normalizes H iff g^-1 * h * g is in H for all generators h of H
                if all((~g * h * g) in H for h in h_gens):
                    n_order += 1
            
            idx_G = G.order() // H.order()
            idx_N = n_order // H.order()
            
            neg_q = bool((idx_G % p) != (idx_N % p))
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: H is a p-subgroup of G",
    "¬Q: index of H in G is not congruent to index of H in N_G(H) mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2