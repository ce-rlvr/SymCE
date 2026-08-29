import sympy as sp

# Standard linear algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (T, U, M) where:
      - T is the matrix of the linear operator on V.
      - U is the matrix whose columns generate the subspace.
      - M is the matrix of the restriction operator T|_U on the generators.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        T, U, M = witness
    except Exception:
        return [False, False, False]
        
    # H1: V is a finite-dimensional vector space
    try:
        h1 = (hasattr(T, 'is_square') and T.is_square and 
              hasattr(U, 'rows') and U.rows == T.rows and 
              hasattr(M, 'is_square') and M.is_square and U.cols == M.rows)
    except Exception:
        h1 = False
        
    # H2: U is a T-invariant subspace of V
    # Formalized as the existence of a restriction matrix M such that T * U == U * M
    try:
        h2 = (T * U == U * M)
    except Exception:
        h2 = False
        
    # neg_Q: The characteristic polynomial of the restriction operator T|_U does NOT divide the characteristic polynomial of T
    try:
        x = sp.Symbol('x')
        pT = T.charpoly(x).as_expr()
        pM = M.charpoly(x).as_expr()
        
        # Check if pM divides pT by computing the remainder
        rem = sp.rem(pT, pM, x)
        
        # If the remainder is not zero, then it does not divide
        neg_q = sp.expand(rem) != 0
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: U is a T-invariant subspace of V",
    "¬Q: The characteristic polynomial of the restriction operator T|_U does not divide the characteristic polynomial of T"
]

N_HYP = 2
NEG_Q_INDEX = 2