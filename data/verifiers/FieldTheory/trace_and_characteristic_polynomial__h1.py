import sympy
from sympy import Matrix, isprime
from sympy.polys.domains import GF
from sympy.polys.polytools import Poly
from sympy.abc import x, t

# Top-level setup for standard algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        q = witness['q']
        n = witness['n']
        modulus = witness['modulus']
        alpha = witness['alpha']
        p = witness['p']
    except Exception:
        return [False, False, False, False]

    # H1: F_{q^n} is an extension field of degree n over F_q
    h1 = False
    try:
        if isinstance(q, int) and isprime(q) and isinstance(n, int) and n >= 1:
            if isinstance(modulus, list) and all(isinstance(c, int) for c in modulus):
                if len(modulus) == n + 1 and (modulus[0] % q) == 1:
                    domain = GF(q)
                    mod_poly = Poly(modulus, x, domain=domain)
                    if mod_poly.is_irreducible:
                        h1 = True
    except Exception:
        h1 = False

    # H2: \alpha is an element of F_{q^n}
    h2 = False
    try:
        if isinstance(alpha, int):
            alpha = [alpha]
        if isinstance(alpha, list) and all(isinstance(c, int) for c in alpha):
            alpha_clean = alpha.copy()
            while len(alpha_clean) > 1 and alpha_clean[0] == 0:
                alpha_clean.pop(0)
            if len(alpha_clean) <= n:
                h2 = True
    except Exception:
        h2 = False

    # H3: p(x) is the characteristic polynomial of \alpha over F_q
    h3 = False
    try:
        if h1 and h2:
            if isinstance(p, list) and all(isinstance(c, int) for c in p):
                if len(p) == n + 1 and (p[0] % q) == 1:
                    domain = GF(q)
                    mod_poly = Poly(modulus, x, domain=domain)
                    alpha_poly = Poly(alpha, x, domain=domain)
                    
                    matrix_cols = []
                    for i in range(n):
                        xi = Poly([1] + [0]*i, x, domain=domain)
                        prod = (alpha_poly * xi) % mod_poly
                        coeffs = [int(domain.to_sympy(c)) for c in prod.all_coeffs()]
                        coeffs = [0]*(n - len(coeffs)) + coeffs
                        matrix_cols.append(coeffs[::-1])
                    
                    M = Matrix(matrix_cols).transpose()
                    char_poly_expr = M.charpoly(t)
                    char_poly_coeffs = char_poly_expr.all_coeffs()
                    
                    char_poly_coeffs_mod_q = [int(c) % q for c in char_poly_coeffs]
                    p_mod_q = [int(c) % q for c in p]
                    
                    if p_mod_q == char_poly_coeffs_mod_q:
                        h3 = True
    except Exception:
        h3 = False

    # neg_Q: The trace Tr_{F_{q^n}/F_q}(\alpha) is NOT equal to the coefficient c_{n-1}
    neg_Q = False
    try:
        if h1 and h2 and isinstance(p, list) and all(isinstance(c, int) for c in p) and len(p) == n + 1:
            domain = GF(q)
            mod_poly = Poly(modulus, x, domain=domain)
            alpha_poly = Poly(alpha, x, domain=domain)
            
            matrix_cols = []
            for i in range(n):
                xi = Poly([1] + [0]*i, x, domain=domain)
                prod = (alpha_poly * xi) % mod_poly
                coeffs = [int(domain.to_sympy(c)) for c in prod.all_coeffs()]
                coeffs = [0]*(n - len(coeffs)) + coeffs
                matrix_cols.append(coeffs[::-1])
            
            M = Matrix(matrix_cols).transpose()
            trace_alpha = int(sum(M[i, i] for i in range(n))) % q
            
            # p(x) = x^n - c_{n-1}x^{n-1} + ...
            # So the coefficient of x^{n-1} is -c_{n-1}, which is p[1]
            c_n_minus_1 = (-int(p[1])) % q
            
            if trace_alpha != c_n_minus_1:
                neg_Q = True
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: F_{q^n} is an extension field of degree n over F_q",
    "H_2: alpha is an element of F_{q^n}",
    "H_3: p(x) is the characteristic polynomial of alpha over F_q",
    "¬Q: The trace Tr_{F_{q^n}/F_q}(alpha) is NOT equal to the coefficient c_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3