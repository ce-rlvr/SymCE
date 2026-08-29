import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - GL(n, C) is the group of n x n invertible matrices with complex entries
      - GL(n, C) is equipped with the subspace topology inherited from C^{n x n}
    Conclusion:
      - GL(n, C) is a connected topological space
      
    The witness is the dimension `n`.
    """
    n = witness
    
    # H_1: GL(n, C) is the group of n x n invertible matrices with complex entries
    # This implies n is a valid dimension (an integer).
    try:
        if isinstance(n, (int, sympy.Integer)):
            n_val = int(n)
            h1 = True
        else:
            h1 = False
            n_val = None
    except Exception:
        h1 = False
        n_val = None
        
    # H_2: GL(n, C) is equipped with the subspace topology...
    # This is a definitional property of the space in this context.
    h2 = True
    
    # ¬Q: GL(n, C) is NOT a connected topological space
    # GL(n, C) is connected for all integers n >= 0.
    try:
        if h1 and n_val >= 0:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: GL(n, \\mathbb{C}) is the group of n \\times n invertible matrices with complex entries",
    "H_2: GL(n, \\mathbb{C}) is equipped with the subspace topology inherited from the standard Euclidean topology on \\mathbb{C}^{n \\times n}",
    "¬Q: GL(n, \\mathbb{C}) is not a connected topological space"
]

N_HYP = 2
NEG_Q_INDEX = 2