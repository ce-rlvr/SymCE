import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    res = [False, False, False]
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) < 2:
            return res
        
        A = sp.Matrix(witness[0])
        B = sp.Matrix(witness[1])
        
        # H_1: A and B are m x n complex matrices
        h1 = (A.shape == B.shape)
        res[0] = h1
        
        if not h1:
            return res
            
        # H_2: sigma_1(A) >= ... >= sigma_min(m,n)(A) are the singular values of A
        # We verify that we can compute and sort the singular values.
        sigma_A = sorted(A.singular_values(), reverse=True)
        res[1] = True
        
        # ¬Q: sum_{i=1}^{min(m,n)} (sigma_i(A) - sigma_i(B))^2 > ||A - B||_F^2
        sigma_B = sorted(B.singular_values(), reverse=True)
        
        lhs = sum((sa - sb)**2 for sa, sb in zip(sigma_A, sigma_B))
        
        diff = A - B
        rhs = sum(x * sp.conjugate(x) for x in diff)
        
        diff_val = lhs - rhs
        
        try:
            # Evaluate numerically to avoid symbolic comparison issues
            diff_num = complex(sp.N(diff_val))
            if abs(diff_num.imag) < 1e-7:
                neg_q = bool(diff_num.real > 1e-7)
            else:
                neg_q = False
        except TypeError:
            # Fallback to symbolic simplification if numerical evaluation fails
            diff_simp = sp.simplify(diff_val)
            if diff_simp.is_real:
                neg_q = bool(diff_simp > 0)
            else:
                neg_q = False
                
        res[2] = neg_q
        
    except Exception:
        pass
        
    return res

CONDITION_LABELS = [
    "H_1: A and B are m x n complex matrices",
    "H_2: sigma_1(A) >= ... >= sigma_min(m,n)(A) are the singular values of A",
    "¬Q: sum_{i=1}^{min(m,n)} (sigma_i(A) - sigma_i(B))^2 > ||A - B||_F^2"
]

N_HYP = 2
NEG_Q_INDEX = 2