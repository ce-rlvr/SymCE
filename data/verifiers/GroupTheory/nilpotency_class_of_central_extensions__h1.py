import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Check if witness is a valid group with lower_central_series method
        if not hasattr(witness, 'lower_central_series'):
            return [False, False]
            
        lcs = witness.lower_central_series()
        
        # If the lower central series does not reach the trivial group, 
        # G is not nilpotent, so G/Z(G) is also not nilpotent.
        if lcs[-1].order() != 1:
            return [False, False]
            
        Z = witness.center()
        
        # Find c: the nilpotency class of G/Z(G)
        # The lower central series of G/Z(G) corresponds to \gamma_i(G) Z(G) / Z(G).
        # It reaches the trivial group when \gamma_{c+1}(G) <= Z(G).
        # In our 0-indexed lcs list, lcs[i] corresponds to \gamma_{i+1}(G).
        c = None
        for i in range(len(lcs)):
            # Check if lcs[i] is a subgroup of Z
            if all(g in Z for g in lcs[i].generators):
                c = i
                break
                
        if c is None:
            return [False, False]
            
        h1 = True
        
        # G's nilpotency class is the length of its lower central series minus 1
        g_class = len(lcs) - 1
        
        # Conclusion Q: G is nilpotent of class c+1
        q = (g_class == c + 1)
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: The quotient group G/Z(G) is nilpotent of class c",
    "¬Q: G is not nilpotent of class c+1"
]

N_HYP = 1
NEG_Q_INDEX = 1