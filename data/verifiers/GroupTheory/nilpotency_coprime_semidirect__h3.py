import math
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics import PermutationGroup

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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, N, H) where G is the internal semidirect 
    product of N and H.
    """
    try:
        # Unpack witness
        G, N, H = witness
        
        # Verify that G, N, H are group objects with required methods
        if not (hasattr(G, 'is_nilpotent') and hasattr(N, 'is_nilpotent') and hasattr(H, 'is_nilpotent')):
            return [False, False, False]
            
        # Verify that G is the internal semidirect product of N and H
        if G.order() != N.order() * H.order():
            return [False, False, False]
            
        for gen in N.generators:
            if gen not in G:
                return [False, False, False]
        for gen in H.generators:
            if gen not in G:
                return [False, False, False]
                
        # Verify that N is a normal subgroup of G
        for g in G.generators:
            for n in N.generators:
                if g * n * g**-1 not in N:
                    return [False, False, False]
                    
        # H_1: N and H are finite groups
        # PermutationGroups in SymPy are finite by definition
        h1 = True
        
        # H_2: The orders |N| and |H| are coprime
        h2 = math.gcd(N.order(), H.order()) == 1
        
        # Evaluate P: G is nilpotent
        P = G.is_nilpotent
        
        # Evaluate Q: N and H are nilpotent, and phi is trivial
        Q1 = N.is_nilpotent
        Q2 = H.is_nilpotent
        
        # phi is trivial iff elements of H commute with elements of N
        phi_trivial = True
        for n in N.generators:
            for h in H.generators:
                if h * n != n * h:
                    phi_trivial = False
                    break
            if not phi_trivial:
                break
                
        Q = Q1 and Q2 and phi_trivial
        
        # ¬Q: The conclusion (P <-> Q) fails
        neg_q = (P != Q)
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: N and H are finite groups",
    "H_2: The orders |N| and |H| are coprime",
    "¬Q: The equivalence between G being nilpotent and (N, H nilpotent and phi trivial) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2