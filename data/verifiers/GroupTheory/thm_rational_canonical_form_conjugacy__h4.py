import sympy as sp
from sympy import Matrix, eye, zeros, Rational

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    F_obj = None
    n = None
    A = None
    B = None
    
    try:
        if isinstance(witness, dict):
            F_obj = witness.get('F', None)
            n = witness.get('n', None)
            A = witness.get('A', None)
            B = witness.get('B', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                A, B = witness
                # If n is not provided, pick an n that mismatches the matrix dimension
                n = A.shape[0] + 1 if hasattr(A, 'shape') else 3
            elif len(witness) == 3:
                n, A, B = witness
            elif len(witness) == 4:
                F_obj, n, A, B = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        if F_obj is not None:
            h1 = getattr(F_obj, 'is_Field', True)
        else:
            # If F is implicit, we assume the matrices are over a field (e.g., QQ)
            h1 = True
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H_3: GL_n(F) is the general linear group of degree n over F
    # This is a definitional context hypothesis.
    h3 = True

    # ¬Q: It is NOT the case that A and B are conjugate in GL_n(F) iff they have the same RCF
    try:
        if hasattr(A, 'shape') and hasattr(B, 'shape'):
            if A.shape == (n, n) and B.shape == (n, n):
                # If A and B are n x n matrices over a field, they are conjugate in GL_n(F) 
                # (i.e., similar) if and only if they have the same rational canonical form.
                # The biconditional holds, so the negation is False.
                neg_q = False
            else:
                # If they are not n x n, they cannot be conjugated by an n x n matrix in GL_n(F).
                conjugate_in_GLn = False
                
                # Check if they have the same rational canonical form
                if A.shape[0] == A.shape[1] and B.shape[0] == B.shape[1]:
                    if A == B:
                        same_rcf = True
                    else:
                        try:
                            same_rcf = A.is_similar(B)
                        except Exception:
                            same_rcf = False
                else:
                    same_rcf = False
                
                # The conclusion fails if the biconditional is false
                neg_q = not (conjugate_in_GLn == same_rcf)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: GL_n(F) is the general linear group of degree n over F",
    "¬Q: It is not the case that A and B are conjugate in GL_n(F) if and only if they have the same rational canonical form"
]

N_HYP = 3
NEG_Q_INDEX = 3