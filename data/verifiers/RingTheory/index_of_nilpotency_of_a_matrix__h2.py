import sympy
from sympy import Matrix, zeros, eye
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If F is a field and A is a nilpotent matrix, then A^n is the zero matrix."
    
    The dropped hypothesis was likely "A is an n x n matrix".
    The witness can be a tuple (A, n) or just a matrix A (in which case n is inferred).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, n = witness
        else:
            A = witness
            # Fallback: if n is not provided, choose n = dim - 1 to make A^n != 0 for a nilpotent matrix of max index
            n = A.shape[0] - 1 if (hasattr(A, 'shape') and A.shape[0] > 0) else 1
    except Exception:
        A = witness
        n = 1

    # H1: F is a field
    # In the context of SymPy, we verify that A is a matrix (which implicitly has elements in a field/ring)
    try:
        h1 = hasattr(A, 'is_square') and hasattr(A, 'shape')
    except Exception:
        h1 = False

    # H2: A is a nilpotent matrix
    # A square matrix of dimension m is nilpotent iff A^m == 0
    try:
        if h1 and A.is_square:
            dim = A.shape[0]
            if dim == 0:
                h2 = True
            else:
                Adim = A**dim
                h2 = True
                for e in Adim:
                    if e.is_zero is True:
                        continue
                    if sympy.simplify(e) == 0:
                        continue
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: A^n is not the zero matrix
    try:
        if h1 and A.is_square:
            dim = A.shape[0]
            if dim == 0:
                neg_q = False
            else:
                An = A**n
                is_zero = True
                for e in An:
                    if e.is_zero is True:
                        continue
                    if sympy.simplify(e) == 0:
                        continue
                    is_zero = False
                    break
                neg_q = not is_zero
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is a nilpotent matrix",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2