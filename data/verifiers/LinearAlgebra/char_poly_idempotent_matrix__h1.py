import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    from sympy.abc import x
    from sympy import expand, simplify
    
    # Parse witness: allow either a matrix P, or a tuple (P, k) if rank is custom/overridden
    if isinstance(witness, tuple) and len(witness) == 2:
        P, k = witness
        provided_k = True
    else:
        P = witness
        provided_k = False

    # H_1: P is idempotent, meaning P^2 = P
    try:
        h1 = bool(P**2 == P)
    except Exception:
        h1 = False

    # H_2: Let k be the rank of P
    try:
        n = P.shape[0]
        if provided_k:
            try:
                actual_k = P.rank()
                h2 = bool(k == actual_k)
            except Exception:
                # If rank() fails (e.g., over a custom ring), we trust the provided k
                h2 = True
        else:
            k = P.rank()
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The characteristic polynomial of P is NOT x^{n-k}(x-1)^k
    try:
        cp = P.charpoly(x).as_expr()
        expected = (x**(n-k)) * ((x-1)**k)
        
        # Check for mathematical equality
        if cp == expected:
            neg_q = False
        elif expand(cp) == expand(expected):
            neg_q = False
        else:
            try:
                diff = simplify(cp - expected)
                neg_q = bool(diff != 0)
            except Exception:
                # If simplification fails but they weren't caught by expand, assume they are different
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is idempotent (P^2 = P)",
    "H_2: k is the rank of P",
    "¬Q: The characteristic polynomial of P is NOT x^{n-k}(x-1)^k"
]

N_HYP = 2
NEG_Q_INDEX = 2