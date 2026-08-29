import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_p_and_int_matrix(witness):
    """
    Extracts the matrix P and the field characteristic p from the witness.
    Converts P to an integer matrix for safe polynomial arithmetic.
    """
    p = 0
    P_raw = witness
    
    if isinstance(witness, tuple) and len(witness) == 2:
        P_raw, p = witness
    elif isinstance(witness, dict) and 'P' in witness and 'p' in witness:
        P_raw, p = witness['P'], witness['p']
        
    if hasattr(P_raw, 'to_Matrix'):
        P_raw = P_raw.to_Matrix()
        
    P = sp.Matrix(P_raw)
    
    # Try to infer p from elements if not explicitly provided
    if p == 0:
        for val in P:
            if isinstance(val, sp.Expr) and val.func == sp.Mod:
                p = int(val.args[1])
                break
            if hasattr(val, 'mod'):
                try:
                    p = int(val.mod)
                    break
                except Exception:
                    pass
                
    if p > 0:
        def to_int(val):
            if isinstance(val, sp.Expr) and val.func == sp.Mod:
                return int(val.args[0]) % p
            if hasattr(val, 'val'):
                return int(val.val) % p
            return int(val) % p
        try:
            P_int = P.applyfunc(to_int)
            return P_int, p
        except Exception:
            pass
            
    return P, 0

def conditions(witness):
    try:
        P, p = get_p_and_int_matrix(witness)
    except Exception:
        return [False, False]
        
    # H_1: P is an n x n projection matrix over a field
    try:
        if not P.is_square:
            h1 = False
        else:
            if p > 0:
                diff = P**2 - P
                h1 = all(val % p == 0 for val in diff)
            else:
                h1 = (P**2 == P)
    except Exception:
        h1 = False

    # ¬Q: The characteristic polynomial of P is NOT x^{n-r}(x-1)^r
    try:
        x_sym = sp.Symbol('x')
        n = P.shape[0]
        
        if p > 0:
            r = sum(P[i, i] for i in range(n)) % p
        else:
            r = P.trace()
            
        r = int(r)
        
        expected_poly = sp.expand((x_sym**(n - r)) * ((x_sym - 1)**r))
        actual_poly = sp.expand(P.charpoly(x_sym).as_expr())
        
        diff_poly = sp.expand(actual_poly - expected_poly)
        
        if p > 0:
            if diff_poly == 0:
                neg_q = False
            else:
                coeffs = sp.Poly(diff_poly, x_sym).coeffs()
                neg_q = not all(c % p == 0 for c in coeffs)
        else:
            if diff_poly == 0:
                neg_q = False
            else:
                neg_q = not sp.simplify(diff_poly).is_zero
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is an n x n projection matrix over a field",
    "¬Q: The characteristic polynomial of P is not x^{n-r}(x-1)^r"
]

N_HYP = 1
NEG_Q_INDEX = 1