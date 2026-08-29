import sympy as sp
from sympy import simplify, Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard objects
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
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    
    Hypothesis:
      - A is an n x n diagonal matrix.
      
    Conclusion:
      - The singular values of A are the absolute values |d_1|, |d_2|, ..., |d_n| sorted in descending order.
      (This means the sequence of singular values is exactly the sequence of absolute values of the diagonal entries,
       which implies the absolute values of the diagonal entries must already be sorted in descending order).
    """
    # H_1: A is an n x n diagonal matrix
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square or not hasattr(witness, 'rows') or not hasattr(witness, 'cols'):
            h1 = False
        else:
            h1 = True
            for i in range(witness.rows):
                for j in range(witness.cols):
                    if i != j and witness[i, j] != 0:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: The singular values of A are NOT the absolute values |d_1|, ..., |d_n| sorted in descending order
    try:
        if not h1:
            neg_q = False
        else:
            sv = witness.singular_values()
            d_abs = [abs(witness[i, i]) for i in range(witness.rows)]
            
            is_equal = True
            if len(sv) != len(d_abs):
                is_equal = False
            else:
                for a, b in zip(sv, d_abs):
                    # Check for exact equality first, fallback to symbolic simplification
                    if a != b and simplify(a - b) != 0:
                        is_equal = False
                        break
            
            # If the sequences are not exactly equal, the conclusion fails.
            neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n diagonal matrix",
    "¬Q: The singular values of A are not the absolute values |d_1|, ..., |d_n| sorted in descending order"
]

N_HYP = 1
NEG_Q_INDEX = 1