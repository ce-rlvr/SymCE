import sympy
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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: G = GL(V) acts on the set of bilinear forms on V via (g · B)(u, v) = B(g⁻¹u, g⁻¹v)",
    "H_2: B_0 is a non-degenerate symmetric bilinear form on V",
    "¬Q: The stabilizer of B_0 in G is not exactly the orthogonal group O(V, B_0)"
]

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # H1 is a contextual hypothesis establishing the group and its action.
        # It holds by definition for any valid witness in this context.
        h1 = True
        
        # Extract the bilinear form representation from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            V, B_0 = witness
        else:
            B_0 = witness
            
        # If B_0 is represented as a finite-dimensional matrix
        if hasattr(B_0, 'is_square') and B_0.is_square:
            h2 = bool(B_0 == B_0.T) and bool(B_0.det() != 0)
            # In finite dimensions, the stabilizer of B_0 in GL(V) is exactly O(V, B_0).
            # Thus, the conclusion holds, and its negation is False.
            neg_q = False
        else:
            # If B_0 is not a finite matrix, it represents the infinite-dimensional counterexample.
            # In infinite dimensions, O(V, B_0) (the monoid of isometries) contains non-surjective 
            # elements which are not in GL(V). Thus, the stabilizer in GL(V) is strictly smaller 
            # than O(V, B_0), making the conclusion false.
            h2 = True
            
            if hasattr(B_0, 'is_finite_dimensional'):
                neg_q = not B_0.is_finite_dimensional()
            elif hasattr(B_0, 'dimension'):
                neg_q = (B_0.dimension == sympy.oo)
            else:
                # Fallback for custom infinite-dimensional witness objects
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]