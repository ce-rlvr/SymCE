import sympy
from sympy import eye, zeros, expand, simplify, Matrix
from sympy.algebras.quaternion import Quaternion

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_identity(M):
    if not hasattr(M, 'is_square') or not M.is_square:
        return False
    
    if hasattr(M, 'as_explicit'):
        try:
            M = M.as_explicit()
        except Exception:
            pass

    n = M.rows
    for i in range(n):
        for j in range(n):
            val = M[i, j]
            expected = 1 if i == j else 0
            
            # Handle quaternions (non-commutative entries)
            if hasattr(val, 'a') and hasattr(val, 'b') and hasattr(val, 'c') and hasattr(val, 'd'):
                if expand(val.a) != expected or expand(val.b) != 0 or expand(val.c) != 0 or expand(val.d) != 0:
                    return False
            else:
                # Handle standard commutative entries
                diff = expand(val - expected)
                if diff != 0:
                    if diff.simplify() != 0:
                        return False
    return True

def is_unitary(M):
    try:
        if isinstance(M, (list, tuple)):
            M = Matrix(M)
        if not hasattr(M, 'is_square') or not M.is_square:
            return False
        
        # M.H computes the conjugate transpose.
        # For matrices over non-commutative rings (like quaternions), 
        # this relies on the elements correctly implementing .conjugate()
        MMH = M * M.H
        MHM = M.H * M
        
        return is_identity(MMH) and is_identity(MHM)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            witness = Matrix(witness)
    except Exception:
        pass
        
    try:
        h1 = is_unitary(witness)
    except Exception:
        h1 = False
        
    try:
        # The conclusion is that U^T is a unitary matrix.
        # We want neg_Q to be True when the conclusion FAILS (i.e., U^T is NOT unitary).
        neg_q = not is_unitary(witness.T)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The transpose matrix U^T is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1