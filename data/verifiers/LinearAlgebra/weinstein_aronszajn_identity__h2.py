import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
    except Exception:
        return [False, False]
        
    # H_1: A is an m x n complex matrix
    try:
        h1 = getattr(A, 'is_Matrix', False)
    except Exception:
        h1 = False
        
    # ¬Q: The matrices AB and BA do NOT have the same non-zero eigenvalues with the same algebraic multiplicities
    try:
        AB = A * B
        BA = B * A
        
        if not getattr(AB, 'is_Matrix', False) or not getattr(BA, 'is_Matrix', False):
            neg_q = True
        elif not AB.is_square or not BA.is_square:
            neg_q = True
        else:
            evals_AB = AB.eigenvals()
            evals_BA = BA.eigenvals()
            
            def is_zero(val):
                if val == 0:
                    return True
                try:
                    if abs(complex(val)) < 1e-12:
                        return True
                except Exception:
                    pass
                return False
                
            nz_AB = {k: v for k, v in evals_AB.items() if not is_zero(k)}
            nz_BA = {k: v for k, v in evals_BA.items() if not is_zero(k)}
            
            def normalize_dict(d):
                norm_d = {}
                for k, v in d.items():
                    try:
                        c = complex(k)
                        norm_k = (round(c.real, 5), round(c.imag, 5))
                    except Exception:
                        norm_k = str(sp.simplify(k))
                    norm_d[norm_k] = norm_d.get(norm_k, 0) + v
                return norm_d
                
            neg_q = (normalize_dict(nz_AB) != normalize_dict(nz_BA))
    except Exception:
        # If multiplication fails (e.g., dimension mismatch) or eigenvals fails, the conclusion is false.
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: AB and BA do not have the same non-zero eigenvalues with the same algebraic multiplicities"
]

N_HYP = 1
NEG_Q_INDEX = 1