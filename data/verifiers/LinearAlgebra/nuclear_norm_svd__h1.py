import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    # H_1: Let \sigma_1, \dots, \sigma_{\min(m,n)} be the singular values of A.
    # This implies A is a matrix for which singular values can be computed.
    try:
        if not hasattr(witness, 'singular_values') or not hasattr(witness, 'shape'):
            return [False, False]
        m, n = witness.shape
        h1 = True
    except Exception:
        return [False, False]
    
    # ¬Q: The nuclear norm ||A||_* is NOT equal to the sum of the singular values.
    try:
        svs = witness.singular_values()
        
        # The nuclear norm is mathematically defined as the sum of the singular values.
        # If a library function for nuclear norm existed, we would use it here.
        # Since sympy does not have a dedicated nuclear norm function, we compute it 
        # via its mathematical definition.
        nuc_norm = sum(svs)
        
        # The formula in the conclusion is the sum of the singular values.
        formula_sum = sum(svs)
        
        # Check if they are unequal
        diff = sympy.simplify(nuc_norm - formula_sum)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a matrix with singular values",
    "¬Q: The nuclear norm is NOT equal to the sum of the singular values"
]

N_HYP = 1
NEG_Q_INDEX = 1