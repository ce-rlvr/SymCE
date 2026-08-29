import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Let G be a group",
    "H_2: The quotient group G/N is a free group",
    "¬Q: G is not isomorphic to N \\rtimes (G/N) or the short exact sequence does not split"
]

N_HYP = 2
NEG_Q_INDEX = 2

def sequence_splits(G, N):
    """
    Checks if the short exact sequence 1 -> N -> G -> G/N -> 1 splits.
    This is equivalent to finding a complement subgroup H in G such that
    |H| = |G| / |N| and H ∩ N = {1}.
    """
    try:
        if N.order() == 1:
            return True
            
        target_order = G.order() // N.order()
        if target_order == 1:
            return True
            
        N_elems = set(N.elements)
        
        # Check 1-generated (cyclic) complements
        for g in G.elements:
            if g.order() == target_order:
                H = PermutationGroup([g])
                if len(set(H.elements).intersection(N_elems)) == 1:
                    return True
                    
        # If the target order is prime, any complement must be cyclic.
        if sympy.isprime(target_order):
            return False
            
        # Check 2-generated complements (sufficient for small groups)
        elements = list(G.elements)
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                g1 = elements[i]
                g2 = elements[j]
                H = PermutationGroup([g1, g2])
                if H.order() == target_order:
                    if len(set(H.elements).intersection(N_elems)) == 1:
                        return True
                        
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: Let G be a group
    h1 = False
    try:
        if hasattr(G, 'elements') or hasattr(G, 'generators'):
            h1 = True
    except Exception:
        pass

    # H_2: The quotient group G/N is a free group
    h2 = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            if G.is_normal(N):
                # For finite groups, the only free group is the trivial group (rank 0)
                if G.order() == N.order():
                    h2 = True
    except Exception:
        pass

    # ¬Q: G is not isomorphic to N \rtimes (G/N) or the short exact sequence does not split
    neg_q = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            if not G.is_normal(N):
                neg_q = True
            else:
                splits = sequence_splits(G, N)
                neg_q = not splits
    except Exception:
        pass

    return [h1, h2, neg_q]