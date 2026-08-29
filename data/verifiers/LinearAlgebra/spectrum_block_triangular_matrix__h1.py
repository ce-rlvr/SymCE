import sympy
from sympy import Matrix, eye, zeros, Symbol, expand, simplify
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_MAC(witness):
    """
    Extracts or constructs M, A, and C from the witness.
    Supports dictionary format or tuple format.
    """
    if isinstance(witness, dict):
        A = Matrix(witness['A'])
        C = Matrix(witness['C'])
        if 'M' in witness:
            M = Matrix(witness['M'])
        else:
            B = Matrix(witness['B'])
            if 'X' in witness:
                X = Matrix(witness['X'])
            elif 'D' in witness:
                X = Matrix(witness['D'])
            elif 'C21' in witness:
                X = Matrix(witness['C21'])
            else:
                X = zeros(C.rows, A.cols)
            M = Matrix.vstack(Matrix.hstack(A, B), Matrix.hstack(X, C))
        return M, A, C
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            return Matrix(witness[0]), Matrix(witness[1]), Matrix(witness[2])
        elif len(witness) == 4:
            A = Matrix(witness[0])
            B = Matrix(witness[1])
            X = Matrix(witness[2])
            C = Matrix(witness[3])
            M = Matrix.vstack(Matrix.hstack(A, B), Matrix.hstack(X, C))
            return M, A, C
    raise ValueError("Unrecognized witness format")

def conditions(witness) -> list[bool]:
    try:
        M, A, C = extract_MAC(witness)
    except Exception:
        return [False, False]
        
    # Check Hypothesis 1: A and C are square matrices
    try:
        h1 = bool(A.is_square and C.is_square)
    except Exception:
        h1 = False
        
    # Check Negated Conclusion: The spectrum of M is NOT exactly the union of the 
    # spectrum of A and the spectrum of C, preserving algebraic multiplicities.
    # This is equivalent to checking if the characteristic polynomial of M is NOT 
    # equal to the product of the characteristic polynomials of A and C.
    try:
        if not M.is_square:
            neg_q = True
        else:
            t = Symbol('t')
            pM = M.charpoly(t).as_expr()
            pA = A.charpoly(t).as_expr()
            pC = C.charpoly(t).as_expr()
            
            diff = expand(pM - pA * pC)
            if diff == 0:
                q = True
            else:
                q = (simplify(diff) == 0)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and C are square matrices",
    "¬Q: The spectrum of M is not exactly the union of the spectrum of A and C preserving algebraic multiplicities"
]

N_HYP = 1
NEG_Q_INDEX = 1