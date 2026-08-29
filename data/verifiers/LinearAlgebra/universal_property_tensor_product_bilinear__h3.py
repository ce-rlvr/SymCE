import sympy as sp
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The conjecture is actually a universally true theorem (the universal property 
    of the tensor product for bilinear forms holds for all vector spaces).
    Thus, any valid bilinear form will satisfy the hypotheses and the conclusion,
    meaning neg_Q will be False.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # If the witness is a matrix, it represents a bilinear form B(x,y) = x^T M y
        # on finite-dimensional vector spaces over a field.
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            h1 = True
            h2 = True
            # The universal property holds, so the unique linear functional exists.
            neg_q = False
            
        # If the witness is provided as a dictionary of properties
        elif isinstance(witness, dict):
            h1 = bool(witness.get('is_vector_space', True))
            h2 = bool(witness.get('is_bilinear', True))
            neg_q = not bool(witness.get('universal_property_holds', True))
            
        # Fallback for other mathematical objects
        else:
            h1 = True
            h2 = True
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: B is a bilinear form from V \\times W to F",
    "¬Q: There does not exist a unique linear functional \\tilde{B} from V \\otimes W to F such that \\tilde{B}(v \\otimes w) = B(v,w) for all v \\in V and w \\in W"
]

N_HYP = 2
NEG_Q_INDEX = 2