import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

# Top-level setup for potential witness expressions
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

def is_minimal_normal(G, N):
    try:
        if callable(N.order):
            n_order = N.order()
        else:
            n_order = N.order
    except Exception:
        return False
        
    # A minimal normal subgroup is non-trivial by standard definition
    if n_order <= 1:
        return False
        
    # Check if N is a subgroup of G
    for g in N.generators:
        if not G.contains(g):
            return False
            
    # Check if N is normal in G
    for g in G.generators:
        for n in N.generators:
            conj = g * n * ~g
            if not N.contains(conj):
                return False
                
    # Check minimality: no proper non-trivial normal subgroup of G is contained in N.
    # We do this by verifying that the normal closure in G of any non-identity element in N equals N.
    elements = []
    for i, x in enumerate(N.generate()):
        if i > 1000:  # Safety limit to prevent hanging on unexpectedly large groups
            return False
        elements.append(x)
        
    for x in elements:
        # x == x**2 is true if and only if x is the identity element
        if x == x**2:
            continue
            
        gens = [x]
        H = PermutationGroup(gens)
        loop_count = 0
        
        # Compute the normal closure of <x> in G
        while True:
            loop_count += 1
            if loop_count > 100:
                break
                
            new_gens = list(H.generators)
            added = False
            for g in G.generators:
                for h in H.generators:
                    conj = g * h * ~g
                    if not H.contains(conj):
                        new_gens.append(conj)
                        added = True
            if not added:
                break
            H = PermutationGroup(new_gens)
            
        if callable(H.order):
            h_order = H.order()
        else:
            h_order = H.order
            
        # If the normal closure of x is strictly smaller than N, then N is not minimal
        if h_order < n_order:
            return False
            
    return True

def conditions(witness):
    """
    Given a witness tuple (G, N), checks if it is a valid counterexample.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h1 = bool(G.is_nilpotent())
        else:
            h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False
        
    # H_2: N is a minimal normal subgroup of G
    try:
        h2 = is_minimal_normal(G, N)
    except Exception:
        h2 = False
        
    # ¬Q: The order of N is not a prime number
    try:
        if callable(N.order):
            n_order = N.order()
        else:
            n_order = N.order
        neg_q = not isprime(n_order)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: N is a minimal normal subgroup of G",
    "¬Q: The order of N is not a prime number"
]

N_HYP = 2
NEG_Q_INDEX = 2