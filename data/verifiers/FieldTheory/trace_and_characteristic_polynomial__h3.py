import sympy
from sympy import Matrix, eye, zeros, Poly
from sympy.ntheory import factorint
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: F_{q^n} is an extension field of degree n over F_q",
    "H_3: p(x) is the characteristic polynomial of alpha over F_q",
    "¬Q: The trace Tr_{F_{q^n}/F_q}(alpha) is not equal to the coefficient c_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # witness is expected to be a tuple: (q, n, alpha, p_poly) or (q, n, alpha, p_poly, x_sym)
    try:
        if len(witness) == 4:
            q, n, alpha, p_poly = witness
            p_expr = sympy.sympify(p_poly)
            free_syms = p_expr.free_symbols
            x_sym = list(free_syms)[0] if free_syms else sympy.Symbol('x')
        elif len(witness) == 5:
            q, n, alpha, p_poly, x_sym = witness
            p_expr = sympy.sympify(p_poly)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: F_q is a finite field (q must be a prime power)
    try:
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H_2: F_{q^n} is an extension field of degree n over F_q
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False

    # H_3: p(x) is the characteristic polynomial of alpha over F_q
    try:
        deg = sympy.degree(p_expr, x_sym)
        is_monic = sympy.LC(p_expr, x_sym) == 1
        
        if hasattr(alpha, 'charpoly'):
            # If alpha is a matrix, use its characteristic polynomial
            expected_p = alpha.charpoly(x_sym).as_expr()
        else:
            # Otherwise, use the field extension definition: prod(x - alpha^(q^i))
            expected_p = 1
            for i in range(n):
                expected_p *= (x_sym - alpha**(q**i))
            expected_p = sympy.expand(expected_p)
            
        diff = sympy.simplify(p_expr - expected_p)
        if diff == 0:
            h3_eq = True
        else:
            try:
                # Check equality modulo q for finite field polynomials
                poly_diff = sympy.Poly(diff, x_sym)
                h3_eq = all(c % q == 0 for c in poly_diff.coeffs())
            except Exception:
                h3_eq = False
                
        h3 = bool((deg == n) and is_monic and h3_eq)
    except Exception:
        h3 = False

    # ¬Q: The trace Tr_{F_{q^n}/F_q}(alpha) is not equal to the coefficient c_{n-1}
    try:
        # p(x) = x^n - c_{n-1}x^{n-1} + ... => c_{n-1} is the negative of the x^{n-1} coefficient
        c_n_minus_1 = -p_expr.coeff(x_sym, n-1)
        
        # Tr_{F_{q^n}/F_q}(alpha) = sum_{i=0}^{n-1} alpha^{q^i}
        trace_alpha = sum(alpha**(q**i) for i in range(n))
        
        # If alpha is a matrix, trace_alpha is a matrix but c_n_minus_1 is a scalar.
        if hasattr(trace_alpha, 'shape') and not hasattr(c_n_minus_1, 'shape'):
            concl = False
        else:
            diff_concl = sympy.simplify(trace_alpha - c_n_minus_1)
            if hasattr(diff_concl, 'is_zero') and diff_concl.is_zero:
                concl = True
            elif diff_concl == 0:
                concl = True
            else:
                try:
                    concl = bool(diff_concl % q == 0)
                except Exception:
                    concl = False
                    
        neg_q = not concl
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]