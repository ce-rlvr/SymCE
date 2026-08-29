import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The matrix A is invertible",
    "H_2: Let \\lambda be an eigenvalue of A",
    "¬Q: The scalar \\lambda^{-1} is not an eigenvalue of A^{-1}, or the multiplicities do not match"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        A, lmbda = witness
    except Exception:
        return [False, False, False]
        
    # H1: The matrix A is invertible.
    try:
        if hasattr(A, 'is_invertible'):
            if callable(A.is_invertible):
                h1 = bool(A.is_invertible())
            else:
                h1 = bool(A.is_invertible)
        else:
            h1 = bool(A.is_square and A.det() != 0)
    except Exception:
        h1 = False
        
    # H2: Let \lambda be an eigenvalue of A.
    try:
        evs_A = A.eigenvals()
        h2 = False
        actual_lmbda = None
        for val in evs_A:
            if val == lmbda:
                h2 = True
                actual_lmbda = val
                break
        if not h2:
            for val in evs_A:
                try:
                    if sp.simplify(val - lmbda) == 0:
                        h2 = True
                        actual_lmbda = val
                        break
                except Exception:
                    pass
    except Exception:
        h2 = False
        
    # Conclusion: \lambda^{-1} is an eigenvalue of A^{-1}, and multiplicities match.
    try:
        A_inv = A.inv()
        evs_A_inv = A_inv.eigenvals()
        
        try:
            lmbda_inv = 1 / lmbda
        except Exception:
            try:
                lmbda_inv = lmbda**(-1)
            except Exception:
                q = False
                lmbda_inv = None
        
        if lmbda_inv is not None:
            q = False
            actual_lmbda_inv = None
            for val in evs_A_inv:
                if val == lmbda_inv:
                    actual_lmbda_inv = val
                    break
            if actual_lmbda_inv is None:
                for val in evs_A_inv:
                    try:
                        if sp.simplify(val - lmbda_inv) == 0:
                            actual_lmbda_inv = val
                            break
                    except Exception:
                        pass
            
            if actual_lmbda_inv is not None:
                am_A = evs_A[actual_lmbda]
                am_A_inv = evs_A_inv[actual_lmbda_inv]
                
                gm_A = 0
                for val, am, vecs in A.eigenvects():
                    match = False
                    if val == actual_lmbda:
                        match = True
                    else:
                        try:
                            if sp.simplify(val - actual_lmbda) == 0:
                                match = True
                        except Exception:
                            pass
                    if match:
                        gm_A = len(vecs)
                        break
                        
                gm_A_inv = 0
                for val, am, vecs in A_inv.eigenvects():
                    match = False
                    if val == actual_lmbda_inv:
                        match = True
                    else:
                        try:
                            if sp.simplify(val - actual_lmbda_inv) == 0:
                                match = True
                        except Exception:
                            pass
                    if match:
                        gm_A_inv = len(vecs)
                        break
                        
                q = (am_A == am_A_inv) and (gm_A == gm_A_inv)
                
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]