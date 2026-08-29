import sympy as sp
import itertools

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_minpoly_degree(alpha, x):
    """Helper to compute the degree of the minimal polynomial of alpha."""
    if hasattr(alpha, 'minimal_polynomial'):
        try:
            return sp.Poly(alpha.minimal_polynomial(x), x).degree()
        except Exception:
            pass
            
    if hasattr(alpha, 'charpoly'):
        cp = alpha.charpoly(x)
        facs = cp.factor_list()
        bases = [f[0] for f in facs[1]]
        max_exps = [f[1] for f in facs[1]]
        ranges = [range(1, e + 1) for e in max_exps]
        
        best_deg = None
        
        for exps in itertools.product(*ranges):
            test_poly = sp.sympify(1)
            for b, e in zip(bases, exps):
                test_poly *= b**e
                
            coeffs = sp.Poly(test_poly, x).all_coeffs()
            
            mat_val = sp.zeros(alpha.rows, alpha.cols)
            d = len(coeffs) - 1
            I = sp.eye(alpha.rows)
            for i, c in enumerate(coeffs):
                power = d - i
                if power == 0:
                    mat_val += c * I
                elif power == 1:
                    mat_val += c * alpha
                else:
                    mat_val += c * (alpha ** power)
                    
            if mat_val.is_zero_matrix:
                deg = sum([sp.Poly(b, x).degree() * e for b, e in zip(bases, exps)])
                if best_deg is None or deg < best_deg:
                    best_deg = deg
        if best_deg is not None:
            return best_deg

    return sp.Poly(sp.minpoly(alpha, x), x).degree()

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple) and len(witness) == 2:
        alpha, n_wit = witness
    else:
        alpha = witness
        n_wit = None

    # H_1: alpha in K is a non-zero element algebraic over F
    try:
        if hasattr(alpha, 'is_zero_matrix'):
            h1 = not alpha.is_zero_matrix
        else:
            h1 = bool(alpha != 0)
    except Exception:
        h1 = False

    # H_2: The minimal polynomial of alpha over F has degree n
    try:
        x = sp.Symbol('x')
        n = get_minpoly_degree(alpha, x)
        if n_wit is not None:
            h2 = (n == n_wit)
        else:
            h2 = (n >= 1)
    except Exception:
        h2 = False

    # neg_Q: alpha^-1 is NOT algebraic over F OR its minimal polynomial does NOT have degree n
    try:
        if hasattr(alpha, 'inv'):
            inv_alpha = alpha.inv()
        else:
            inv_alpha = sp.sympify(1) / alpha
            
        inv_n = get_minpoly_degree(inv_alpha, x)
        q = (inv_n == n)
    except Exception:
        # If alpha is not invertible (e.g., a zero divisor matrix), the conclusion fails.
        q = False

    neg_q = not q

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is a non-zero element algebraic over F",
    "H_2: The minimal polynomial of alpha over F has degree n",
    "¬Q: alpha^-1 is not algebraic over F or its minimal polynomial does not have degree n"
]

N_HYP = 2
NEG_Q_INDEX = 2