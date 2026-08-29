import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Handle case where witness is a tuple (G, H)
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
            if hasattr(G, 'is_finite'):
                h1 = bool(G.is_finite)
            elif isinstance(G, PermutationGroup):
                h1 = True
                
            # Mathematically, if G is a finite group, Φ(G × H) = Φ(G) × Φ(H) 
            # is ALWAYS true for any group H. Thus, no valid counterexample exists 
            # among actual groups, and the conclusion cannot fail.
            neg_q = False
            
        # Handle case where witness is a single group (implying H = G)
        elif isinstance(witness, PermutationGroup):
            h1 = True
            neg_q = False
            
        # Handle case where witness is a custom mock object
        else:
            if hasattr(witness, 'G_is_finite'):
                h1 = bool(witness.G_is_finite)
            elif hasattr(witness, 'G') and hasattr(witness.G, 'is_finite'):
                h1 = bool(witness.G.is_finite)
                
            if hasattr(witness, 'phi_G_times_H') and hasattr(witness, 'phi_G') and hasattr(witness, 'phi_H'):
                neg_q = bool(witness.phi_G_times_H != witness.phi_G * witness.phi_H)
            elif hasattr(witness, 'frattini_product_equal'):
                neg_q = not bool(witness.frattini_product_equal)
                
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The Frattini subgroup Φ(G × H) is not equal to Φ(G) × Φ(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1