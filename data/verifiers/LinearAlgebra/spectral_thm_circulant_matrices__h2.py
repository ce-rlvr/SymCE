import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: C is an n x n complex circulant matrix",
    "¬Q: C is NOT unitarily diagonalizable by F, meaning F C F^* is NOT a diagonal matrix containing the eigenvalues of C"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness can be just the matrix C, or a tuple (C, F) where F is the matrix to test.
        if isinstance(witness, tuple) and len(witness) == 2:
            C, F = witness
        else:
            C = witness
            n = C.rows
            # Construct the standard discrete Fourier transform matrix if F is not provided
            omega = sp.exp(-2 * sp.I * sp.pi / n)
            F = sp.Matrix(n, n, lambda j, k: omega**(j * k) / sp.sqrt(n))
    except Exception:
        return [False, False]

    # H_1: C is an n x n complex circulant matrix
    h1 = False
    try:
        if getattr(C, 'is_Matrix', False) and C.rows == C.cols:
            n = C.rows
            is_circ = True
            for i in range(n):
                for j in range(n):
                    diff = (C[i, j] - C[0, (j - i) % n]).expand()
                    if diff != 0 and sp.simplify(diff) != 0:
                        is_circ = False
                        break
                if not is_circ:
                    break
            h1 = is_circ
    except Exception:
        h1 = False

    # neg_Q: C is NOT unitarily diagonalizable by F, meaning F C F^* is NOT a diagonal matrix containing the eigenvalues of C
    neg_q = False
    try:
        n = C.rows
        I = sp.eye(n)
        
        # Check if F is unitary (F * F^* = I)
        diff_unitary = (F * F.H - I).expand()
        is_unitary = True
        for i in range(n):
            for j in range(n):
                val = diff_unitary[i, j]
                if val != 0 and sp.simplify(val) != 0:
                    is_unitary = False
                    break
            if not is_unitary:
                break
        
        if not is_unitary:
            # If F is not unitary, C is not unitarily diagonalizable by F
            neg_q = True
        else:
            # Check if F * C * F^* is a diagonal matrix
            D = (F * C * F.H).expand()
            is_diag = True
            for i in range(n):
                for j in range(n):
                    if i != j:
                        val = D[i, j]
                        if val != 0 and sp.simplify(val) != 0:
                            is_diag = False
                            break
                if not is_diag:
                    break
            
            if not is_diag:
                neg_q = True
            else:
                # If F is unitary and F*C*F^* is diagonal, then F*C*F^* is similar to C.
                # Similar matrices share the same eigenvalues, and the eigenvalues of a 
                # diagonal matrix are exactly its diagonal entries. Thus, it mathematically 
                # must contain the eigenvalues of C.
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]