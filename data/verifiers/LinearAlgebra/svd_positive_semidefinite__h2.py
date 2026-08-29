import sympy
from sympy import Matrix, eye, zeros, re, im

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: A is an n x n matrix
    try:
        if not isinstance(witness, Matrix):
            return [False, False, False, False]
        if witness.shape[0] != witness.shape[1]:
            return [False, False, False, False]
        h1 = True
    except Exception:
        return [False, False, False, False]
        
    # H2: A is Hermitian
    try:
        h2 = bool(witness == witness.H)
    except Exception:
        h2 = False
        
    # H3: A is positive semi-definite
    try:
        evs = witness.eigenvals(multiple=True)
        h3 = True
        for e in evs:
            if sympy.im(e) != 0 or sympy.re(e) < 0:
                h3 = False
                break
    except Exception:
        h3 = False
        
    # neg_Q: The conclusion fails at the witness
    try:
        neg_q = False
        
        # Compute the spectral decomposition A = P D P^-1
        P, D = witness.diagonalize()
        diag_elements = []
        for i in range(D.shape[0]):
            val = sympy.simplify(D[i, i])
            # SVD requires Sigma to be real
            if sympy.im(val) != 0:
                neg_q = True
                break
            diag_elements.append(sympy.re(val))
            
        if not neg_q:
            # SVD requires Sigma to be sorted in descending order
            if diag_elements != sorted(diag_elements, reverse=True):
                neg_q = True
            else:
                # SVD requires Sigma to have non-negative entries
                if any(d < 0 for d in diag_elements):
                    neg_q = True
                else:
                    # Check if singular values are equal to eigenvalues
                    svs = witness.singular_values()
                    svs_sorted = sorted([sympy.re(s) for s in svs], reverse=True)
                    evs_sorted = sorted(diag_elements, reverse=True)
                    if svs_sorted != evs_sorted:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: A is Hermitian",
    "H_3: A is positive semi-definite",
    "¬Q: The spectral decomposition is not an SVD, or singular values != eigenvalues"
]

N_HYP = 3
NEG_Q_INDEX = 3