import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Convert list of lists to sympy Matrix if necessary
        if isinstance(witness, list):
            witness = Matrix(witness)
            
        # H_1: A is an n x n matrix with real entries
        if not hasattr(witness, "rows") or not hasattr(witness, "cols"):
            return [False, False]
        if witness.rows != witness.cols:
            return [False, False]
        
        h1_ok = True
        for val in witness:
            if val.is_real is False:
                h1_ok = False
                break
            if val.is_real is None:
                try:
                    c = complex(val)
                    if abs(c.imag) > 1e-9:
                        h1_ok = False
                        break
                except Exception:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    try:
        def is_nonneg_real(e):
            if e.is_real is False:
                return False
            if e.is_real is True:
                return bool(e >= 0)
            try:
                c = complex(e)
                return abs(c.imag) < 1e-9 and c.real >= -1e-9
            except Exception:
                return False

        A = witness
        
        # A matrix is positive semidefinite if x^T A x >= 0 for all x.
        # This is equivalent to its symmetric part (A + A^T)/2 being positive semidefinite,
        # which means all eigenvalues of the symmetric part are >= 0.
        A_sym = (A + A.T) / 2
        
        is_psd = True
        for e in A_sym.eigenvals().keys():
            if not is_nonneg_real(e):
                is_psd = False
                break
                
        # Check if all eigenvalues of A itself are >= 0
        all_eig_nonneg = True
        for e in A.eigenvals().keys():
            if not is_nonneg_real(e):
                all_eig_nonneg = False
                break
                
        # ¬Q: The equivalence fails (one is true and the other is false)
        neg_q_ok = (is_psd != all_eig_nonneg)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "¬Q: The equivalence between being positive semidefinite and having all eigenvalues >= 0 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1