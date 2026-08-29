import sympy
from sympy import Poly, symbols, GF, isprime
from sympy.ntheory import factorint

# Top-level setup
x = symbols('x')

def rank_GF(matrix, q):
    """Compute the rank of a matrix over GF(q) using Gaussian elimination."""
    M = [list(row) for row in matrix]
    rows = len(M)
    if rows == 0: 
        return 0
    cols = len(M[0])
    rank = 0
    for c in range(cols):
        pivot = -1
        for r in range(rank, rows):
            if M[r][c] % q != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        # Swap rows
        M[rank], M[pivot] = M[pivot], M[rank]
        # Normalize pivot row
        inv = pow(M[rank][c], q - 2, q)
        for i in range(cols):
            M[rank][i] = (M[rank][i] * inv) % q
        # Eliminate other rows
        for r in range(rows):
            if r != rank and M[r][c] % q != 0:
                factor = M[r][c]
                for i in range(cols):
                    M[r][i] = (M[r][i] - factor * M[rank][i]) % q
        rank += 1
    return rank

def min_poly_degree(q, n, P_coeffs, alpha_coeffs):
    """Find the degree of the minimal polynomial of alpha over GF(q)."""
    P = Poly(P_coeffs, x, domain=GF(q))
    alpha = Poly(alpha_coeffs, x, domain=GF(q))
    
    vs = []
    current = Poly([1], x, domain=GF(q))
    for i in range(n + 1):
        # Extract coefficients from lowest to highest degree, pad to length n
        coeffs = current.all_coeffs()[::-1]
        coeffs = coeffs + [0] * (n - len(coeffs))
        coeffs = [int(c) % q for c in coeffs]
        vs.append(coeffs)
        current = (current * alpha).rem(P)
        
    for k in range(1, n + 1):
        # Form matrix with columns v_0, v_1, ..., v_k
        M = []
        for r in range(n):
            row = [vs[c][r] for c in range(k + 1)]
            M.append(row)
        # If columns are linearly dependent, we found the minimal polynomial degree
        if rank_GF(M, q) < k + 1:
            return k
    return n

def conditions(witness):
    """
    Check if the witness is a valid counterexample.
    Expected witness format: (q, n, P_coeffs, alpha_coeffs, d)
    where:
      - q: size of the base field (must be prime for this verifier)
      - n: degree of the extension
      - P_coeffs: coefficients of the irreducible polynomial defining F_{q^n}
      - alpha_coeffs: coefficients of the element alpha in F_{q^n}
      - d: the claimed degree of the minimal polynomial
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            P_coeffs = witness.get('P_coeffs')
            alpha_coeffs = witness.get('alpha_coeffs')
            d = witness.get('d')
        else:
            q, n, P_coeffs, alpha_coeffs, d = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        if isinstance(q, int) and q > 1:
            h1 = (len(factorint(q)) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: F_{q^n} is an extension field of degree n over F_q
    try:
        # We restrict to prime q to easily perform polynomial arithmetic over GF(q)
        if isprime(q) and isinstance(n, int) and n >= 1 and isinstance(P_coeffs, list):
            P = Poly(P_coeffs, x, domain=GF(q))
            h2 = (P.degree() == n and P.is_irreducible)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: \alpha is an element of F_{q^n}
    try:
        if isinstance(alpha_coeffs, list) and all(isinstance(c, int) for c in alpha_coeffs):
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The degree of the minimal polynomial of \alpha over F_q is NOT equal to d
    try:
        if isprime(q) and h2 and h3 and isinstance(d, int):
            deg = min_poly_degree(q, n, P_coeffs, alpha_coeffs)
            neg_q = (deg != d)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^n} is an extension field of degree n over F_q",
    "H_3: alpha is an element of F_{q^n}",
    "¬Q: The degree of the minimal polynomial of alpha over F_q is not equal to d"
]

N_HYP = 3
NEG_Q_INDEX = 3