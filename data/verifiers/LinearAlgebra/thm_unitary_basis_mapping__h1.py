import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    'U is a unitary matrix if and only if for every orthonormal basis of C^n, 
    the set {Uv_1, ..., Uv_n} is an orthonormal basis of C^n'
    
    The conjecture is false because it drops the hypothesis that U is an n x n matrix.
    A valid counterexample is a unitary matrix U of size m x m where m != n.
    The witness can be a tuple (U, n) or just U (in which case n is chosen to be m + 1).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            U_raw, n = witness
        else:
            U_raw = witness
            n = None
            
        if not isinstance(U_raw, sp.MatrixBase):
            try:
                U = sp.Matrix(U_raw)
            except Exception:
                # Fallback for scalars
                U = sp.Matrix([[U_raw]])
        else:
            U = U_raw
            
        if n is None:
            n = U.shape[0] + 1
            
        # Evaluate Left Side: "U is a unitary matrix"
        if not U.is_square:
            left = False
        else:
            m = U.shape[0]
            prod = U.H * U
            if prod == sp.eye(m):
                left = True
            else:
                left = bool(sp.simplify(prod) == sp.eye(m))
                
        # Evaluate Right Side: "U maps every ONB of C^n to an ONB of C^n"
        # This is true if and only if U is an n x n unitary matrix.
        if U.shape == (n, n):
            right = left
        else:
            right = False
            
        # The conclusion fails if the equivalence does not hold
        neg_q = bool(left != right)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: U is a unitary matrix XOR U maps every ONB of C^n to an ONB of C^n"
]
N_HYP = 0
NEG_Q_INDEX = 0