import sympy
from sympy.matrices import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "The tensor product of a non-degenerate bilinear form B_1 and any bilinear form B_2 
    is non-degenerate."
    
    The witness should be a tuple of two square SymPy matrices (B1, B2) representing 
    the bilinear forms on V_1 and V_2 respectively.
    """
    # H_1: V_1 and V_2 are finite-dimensional vector spaces over a field F
    # We verify this by checking if the witness provides two square matrices.
    try:
        h1 = (isinstance(witness, tuple) and len(witness) == 2 and 
              hasattr(witness[0], 'is_square') and witness[0].is_square and 
              hasattr(witness[1], 'is_square') and witness[1].is_square and
              hasattr(witness[0], 'det') and hasattr(witness[1], 'det') and
              hasattr(witness[0], 'shape') and hasattr(witness[1], 'shape'))
    except Exception:
        h1 = False

    # H_2: B_1 is a non-degenerate bilinear form on V_1
    try:
        if h1:
            h2 = bool(witness[0].det() != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The tensor product bilinear form B_1 \otimes B_2 is degenerate on V_1 \otimes V_2
    # The determinant of the Kronecker product of an n x n matrix A and an m x m matrix B
    # is det(A)^m * det(B)^n. The form is degenerate if this determinant is 0.
    try:
        if h1:
            n = witness[0].shape[0]
            m = witness[1].shape[0]
            det_tensor = (witness[0].det() ** m) * (witness[1].det() ** n)
            neg_q = bool(det_tensor == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V_1 and V_2 are finite-dimensional vector spaces over a field F",
    "H_2: B_1 is a non-degenerate bilinear form on V_1",
    "¬Q: The tensor product bilinear form B_1 \\otimes B_2 is degenerate on V_1 \\otimes V_2"
]

N_HYP = 2
NEG_Q_INDEX = 2