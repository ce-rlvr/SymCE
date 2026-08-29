import sympy as sp
from sympy.ntheory import isprime, factorint

# Top-level setup
x, y, z, t = sp.symbols('x y z t')
p, q, n_sym = sp.symbols('p q n')

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: F_{q^n} is a finite field extension of F_q of degree n",
    "H_2: B is the bilinear form defined by B(x, y) = Tr_{F_{q^n}/F_q}(xy)",
    "¬Q: The bilinear form B is degenerate"
]

def conditions(witness):
    try:
        p_val = None
        coeffs = None
        n = None
        
        # We handle two types of witnesses:
        # 1. (q, n) where q is a prime power, n is degree. This is a finite field.
        # 2. (p, poly) where p is prime, poly is the minimal polynomial of the extension.
        if isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            if isinstance(a, int) and isinstance(b, int):
                q_val, n_val = a, b
                factors = factorint(q_val)
                if len(factors) == 1:
                    p_val = list(factors.keys())[0]
                    # For finite fields, the trace form is always non-degenerate
                    return [True, True, False]
            
            if isinstance(a, int):
                p_cand = a
                poly_cand = b
            elif isinstance(b, int):
                p_cand = b
                poly_cand = a
            else:
                p_cand = None
                poly_cand = None
                
            if p_cand is not None:
                p_val = p_cand
                if isinstance(poly_cand, list):
                    coeffs = poly_cand
                elif hasattr(poly_cand, 'all_coeffs'):
                    coeffs = poly_cand.all_coeffs()
                elif isinstance(poly_cand, sp.Expr):
                    free_vars = poly_cand.free_symbols
                    if len(free_vars) == 1:
                        poly = sp.Poly(poly_cand, list(free_vars)[0])
                        coeffs = poly.all_coeffs()
                    elif len(free_vars) > 1:
                        # Guess the generator is the one with highest degree
                        gen = max(free_vars, key=lambda v: sp.degree(poly_cand, v))
                        poly = sp.Poly(poly_cand, gen)
                        coeffs = poly.all_coeffs()
                        
        if p_val is None or coeffs is None:
            return [False, False, False]
            
        if not isprime(p_val):
            return [False, False, False]
            
        n = len(coeffs) - 1
        if n < 1:
            return [False, False, False]
            
        if coeffs[0] != 1:
            lead = coeffs[0]
            coeffs = [c / lead for c in coeffs]
            
        # Basic sanity check for irreducibility (non-zero constant term)
        if n > 1 and sp.expand(coeffs[-1]) == 0:
            return [False, False, False]
            
        # Compute Newton sums S_k = Tr(X^k)
        S = [0] * (2 * n - 1)
        S[0] = n
        for k in range(1, 2 * n - 1):
            if k < n:
                term1 = k * coeffs[k]
                term2 = sum(coeffs[i] * S[k - i] for i in range(1, k))
                S[k] = -term1 - term2
            else:
                term2 = sum(coeffs[i] * S[k - i] for i in range(1, n + 1))
                S[k] = -term2
                
        # Construct trace form matrix B
        B = sp.zeros(n, n)
        for i in range(n):
            for j in range(n):
                B[i, j] = S[i + j]
                
        det_B = B.det()
        
        # Check if det_B is identically 0 mod p
        expr = sp.expand(det_B)
        is_deg = True
        if expr != 0:
            if isinstance(expr, (int, sp.Integer)):
                is_deg = (expr % p_val == 0)
            elif hasattr(expr, 'as_coefficients_dict'):
                coeffs_dict = expr.as_coefficients_dict()
                for coeff in coeffs_dict.values():
                    if hasattr(coeff, 'p') and hasattr(coeff, 'q'):
                        if coeff.p % p_val != 0:
                            is_deg = False
                            break
                    elif isinstance(coeff, (int, float)):
                        if int(coeff) % p_val != 0:
                            is_deg = False
                            break
                    else:
                        is_deg = False
                        break
            else:
                is_deg = False
                
        h1 = True
        h2 = True
        neg_q = is_deg
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]