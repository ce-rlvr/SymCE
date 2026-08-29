import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: Let p(x) = x^n + c_1 x^{n-1} + ... + c_n be the characteristic polynomial of A
    h1 = False
    try:
        if hasattr(witness, 'charpoly') and hasattr(witness, 'shape'):
            dummy_x = sp.Dummy('x')
            p = witness.charpoly(dummy_x)
            n = witness.shape[0]
            coeffs = p.all_coeffs()
            if len(coeffs) == n + 1 and coeffs[0] == 1:
                h1 = True
    except Exception:
        h1 = False

    # H2: Let t_k = tr(A^k) for 1 <= k <= n
    h2 = False
    try:
        if hasattr(witness, 'trace') and hasattr(witness, 'shape'):
            n = witness.shape[0]
            t = []
            for k in range(1, n + 1):
                t.append((witness**k).trace())
            if len(t) == n:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: For each 1 <= k <= n, the coefficient c_k satisfies k c_k + sum_{i=1}^k t_i c_{k-i} = 0, where c_0 = 1
    neg_q = False
    try:
        if h1 and h2:
            dummy_x = sp.Dummy('x')
            p = witness.charpoly(dummy_x)
            coeffs = p.all_coeffs() # [c_0, c_1, ..., c_n]
            n = witness.shape[0]
            
            # t[i] will store tr(A^i), with t[0] = 0 for 1-based indexing convenience
            t = [0] + [(witness**k).trace() for k in range(1, n + 1)]
            
            for k in range(1, n + 1):
                c_k = coeffs[k]
                sum_term = sum(t[i] * coeffs[k - i] for i in range(1, k + 1))
                val = k * c_k + sum_term
                
                # Expand the expression to check if it simplifies to zero.
                # This correctly handles non-commutative symbols where terms like a*b and b*a do not cancel.
                val_simp = sp.expand(val)
                if val_simp != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is the characteristic polynomial of A",
    "H_2: t_k = tr(A^k) is defined for 1 <= k <= n",
    "¬Q: k c_k + sum_{i=1}^k t_i c_{k-i} != 0 for some k"
]

N_HYP = 2
NEG_Q_INDEX = 2