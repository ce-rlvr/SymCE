import sympy
from sympy import Matrix, eye, zeros, Rational
from sympy.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Parse the witness. It should provide both A and B0.
        if isinstance(witness, dict):
            A = witness.get('A')
            if 'B0' in witness:
                B0 = witness['B0']
            elif 'B_seq' in witness:
                B0 = witness['B_seq'][0]
            else:
                B0 = None
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                A, B0 = witness
            elif len(witness) == 3:
                A, B_seq, c_seq = witness
                B0 = B_seq[0]
            else:
                A, B0 = None, None
        else:
            A, B0 = None, None

        # Convert to SymPy matrices if they aren't already
        if A is not None and not isinstance(A, MatrixBase):
            try:
                A = Matrix(A)
            except Exception:
                pass
        if B0 is not None and not isinstance(B0, MatrixBase):
            try:
                B0 = Matrix(B0)
            except Exception:
                pass
            
        # H1: A is an n x n matrix (n >= 1)
        if A is not None and isinstance(A, MatrixBase):
            h1 = (A.shape[0] == A.shape[1]) and (A.shape[0] >= 1)
            
        # H2: B0 is provided and is an n x n matrix, allowing the sequence to be defined
        if h1 and B0 is not None and isinstance(B0, MatrixBase):
            h2 = (B0.shape == A.shape)
            
    except Exception:
        pass

    try:
        if h1 and h2:
            n = A.shape[0]
            B_k = B0
            I = eye(n)
            
            # Compute the sequence recursively
            for k in range(1, n + 1):
                c_k = -Rational(1, k) * (A * B_k).trace()
                B_k = A * B_k + c_k * I
            
            # Simplify to handle any symbolic entries
            B_k = sympy.simplify(B_k)
            
            # ¬Q: The final matrix B_n is NOT the zero matrix
            neg_q = bool(B_k != zeros(n, n))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field of characteristic zero",
    "H_2: The sequence c_k and B_k can be defined recursively (B0 is provided)",
    "¬Q: The final matrix B_n is not the zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2