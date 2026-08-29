import sympy
from sympy import Matrix, eye, zeros
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_degenerate_algebra(q, coeffs):
    """
    Computes whether the trace bilinear form of the algebra F_q[x]/(f(x)) is degenerate,
    where f(x) is defined by the given monic polynomial coefficients.
    """
    n = len(coeffs) - 1
    if n < 1 or n > 50:
        return False
    
    # Companion matrix for multiplication by x
    C = Matrix.zeros(n, n)
    for i in range(n - 1):
        C[i + 1, i] = 1
    for i in range(n):
        C[i, n - 1] = -int(coeffs[n - i]) % q
        
    # Compute traces of multiplication by x^k for k = 0 to 2n-2
    traces = []
    C_k = Matrix.eye(n)
    for k in range(2 * n - 1):
        tr = sum(C_k[i, i] for i in range(n)) % q
        traces.append(tr)
        C_k = (C_k * C).applyfunc(lambda val: val % q)
        
    # Construct the trace form matrix M_{ij} = Tr(x^{i+j})
    M = Matrix.zeros(n, n)
    for i in range(n):
        for j in range(n):
            M[i, j] = traces[i + j]
            
    det = M.det() % q
    return det == 0

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (q, ext), where:
      - q is the size of the finite field F_q.
      - ext represents the extension F_{q^n}, given as an integer degree n, 
        a polynomial (list of coeffs or sympy expression), or a trace form matrix.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        q, ext = witness
        
        # H_1: F_q is a finite field (q must be a prime power)
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = len(factors) == 1
            
        h2 = False
        neg_q = False
        
        # H_2 & ¬Q evaluation based on the type of extension provided
        if isinstance(ext, int):
            h2 = ext >= 1
            # The trace form of a finite field extension is mathematically NEVER degenerate.
            neg_q = False
            
        elif isinstance(ext, (list, tuple)) and not isinstance(ext[0], (list, tuple)):
            h2 = len(ext) >= 2
            if h1 and h2:
                try:
                    coeffs = list(ext)
                    lead = coeffs[0]
                    if lead != 0:
                        inv = pow(int(lead), -1, q)
                        coeffs = [(int(c) * inv) % q for c in coeffs]
                        neg_q = is_degenerate_algebra(q, coeffs)
                except (ValueError, TypeError):
                    neg_q = False
                    
        elif isinstance(ext, sympy.Poly):
            h2 = ext.degree() >= 1
            if h1 and h2:
                try:
                    coeffs = ext.all_coeffs()
                    lead = coeffs[0]
                    if lead != 0:
                        inv = pow(int(lead), -1, q)
                        coeffs = [(int(c) * inv) % q for c in coeffs]
                        neg_q = is_degenerate_algebra(q, coeffs)
                except (ValueError, TypeError):
                    neg_q = False
                    
        elif hasattr(ext, 'free_symbols') and len(ext.free_symbols) == 1:
            try:
                poly_ext = sympy.Poly(ext)
                h2 = poly_ext.degree() >= 1
                if h1 and h2:
                    coeffs = poly_ext.all_coeffs()
                    lead = coeffs[0]
                    if lead != 0:
                        inv = pow(int(lead), -1, q)
                        coeffs = [(int(c) * inv) % q for c in coeffs]
                        neg_q = is_degenerate_algebra(q, coeffs)
            except Exception:
                h2 = False
                
        elif isinstance(ext, Matrix) or (isinstance(ext, (list, tuple)) and len(ext) > 0 and isinstance(ext[0], (list, tuple))):
            try:
                M = Matrix(ext)
                h2 = M.rows == M.cols and 1 <= M.rows <= 50
                if h1 and h2:
                    det = M.det()
                    if det.is_number:
                        neg_q = (int(det) % q) == 0
            except Exception:
                h2 = False
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: B is the trace bilinear form on F_{q^n} over F_q",
    "¬Q: The bilinear form B is degenerate"
]
N_HYP = 2
NEG_Q_INDEX = 2