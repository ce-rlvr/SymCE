import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

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

def is_sylow_subgroup(G, H):
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            return False
        
        # Check if H is a subgroup of G
        for g in H.generators:
            if g not in G:
                return False
                
        oG = G.order()
        oH = H.order()
        
        # Lagrange's theorem check
        if oG % oH != 0:
            return False
            
        # Trivial group is a Sylow p-subgroup for any prime p not dividing |G|
        if oH == 1:
            return True
            
        # Check if |H| is a prime power p^k
        f = factorint(oH)
        if len(f) != 1:
            return False
            
        p = list(f.keys())[0]
        
        # Check if p divides |G| / |H|
        if (oG // oH) % p == 0:
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness (G, P, Q), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        # Allow witness to be (G, P, Q) or (G, p, P, Q) by taking the first and last two elements
        if len(witness) < 3:
            return [False, False, False]
        G = witness[0]
        P = witness[-2]
        Q = witness[-1]
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False
        
    # H_2: P and Q are Sylow p-subgroups of G
    try:
        h2_ok = is_sylow_subgroup(G, P) and is_sylow_subgroup(G, Q)
    except Exception:
        h2_ok = False
        
    # ¬Q: P is not isomorphic to Q
    try:
        if P.order() != Q.order():
            neg_q_ok = True
        else:
            if hasattr(P, 'is_isomorphic'):
                neg_q_ok = not P.is_isomorphic(Q)
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P and Q are Sylow p-subgroups of G",
    "¬Q: P is not isomorphic to Q"
]

N_HYP = 2
NEG_Q_INDEX = 2