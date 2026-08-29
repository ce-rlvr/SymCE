import sympy
from sympy import Matrix, MatrixBase, eye, zeros
from sympy.ntheory import isprime

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (A, p) where A is a matrix and p is the prime characteristic 
    of the field F (or p=0 for characteristic 0). It can also just be a matrix A if the 
    elements natively evaluate to 0 (e.g., using Mod or GF elements).
    """
    # Extract A and p
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A_input, p = witness
        else:
            A_input = witness
            p = 0
    except Exception:
        return [False, False, False]

    # H1: A is an n \times n matrix over F
    try:
        if not isinstance(A_input, MatrixBase):
            try:
                A = Matrix(A_input)
            except Exception:
                A = A_input
        else:
            A = A_input
            
        if not isinstance(A, MatrixBase):
            h1 = False
        else:
            h1 = A.is_square and (p == 0 or isprime(p))
    except Exception:
        h1 = False

    # H2: The trace of A^k is zero for all integers k such that 1 \le k \le n
    try:
        if h1:
            n = A.shape[0]
            h2 = True
            for k in range(1, n + 1):
                Ak = A**k
                tr = Ak.trace()
                if p > 0:
                    if tr % p != 0:
                        h2 = False
                        break
                else:
                    if tr != 0:
                        h2 = False
                        break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: A is not nilpotent
    try:
        if h1:
            n = A.shape[0]
            An = A**n
            if p > 0:
                is_nilp = all(x % p == 0 for x in An)
            else:
                is_nilp = all(x == 0 for x in An)
            neg_q = not is_nilp
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over F",
    "H_2: The trace of A^k is zero for all integers k such that 1 <= k <= n",
    "¬Q: A is not a nilpotent matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2