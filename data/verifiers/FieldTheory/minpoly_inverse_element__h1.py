import sympy
from sympy import Symbol, Poly, zeros, eye, simplify, expand, Matrix
from sympy import minimal_polynomial

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    x = Symbol('x')
    try:
        if isinstance(witness, dict):
            alpha = witness['alpha']
            f = witness.get('f', None)
            x_sym = witness.get('x', x)
        else:
            alpha = witness
            f = None
            x_sym = x
            
        if f is None:
            if hasattr(alpha, 'minimal_polynomial'):
                f = alpha.minimal_polynomial(x_sym)
            else:
                f = minimal_polynomial(alpha, x_sym)
            
            f = Poly(f, x_sym).monic()
        else:
            f = Poly(f, x_sym)
    except Exception:
        return [False, False, False]

    # H1: alpha is a non-zero element algebraic over F
    try:
        if hasattr(alpha, 'is_zero_matrix'):
            is_zero = alpha.is_zero_matrix
        elif hasattr(alpha, 'is_zero'):
            is_zero = alpha.is_zero
        else:
            is_zero = (alpha == 0)
            
        h1 = not is_zero
    except Exception:
        h1 = False

    # H2: f(x) is the minimal polynomial of alpha over F
    try:
        if f.LC() != 1:
            h2 = False
        else:
            n = f.degree()
            coeffs = f.all_coeffs()
            
            if hasattr(alpha, 'rows'):
                val = zeros(alpha.rows, alpha.cols)
                I = eye(alpha.rows)
                for i, c in enumerate(coeffs):
                    power = n - i
                    if power == 0:
                        val += c * I
                    else:
                        val += c * (alpha ** power)
                is_root = val.is_zero_matrix
            else:
                val = 0
                for i, c in enumerate(coeffs):
                    power = n - i
                    val += c * (alpha ** power)
                is_root = simplify(val) == 0
                
            if not is_root:
                h2 = False
            else:
                if hasattr(alpha, 'minimal_polynomial'):
                    min_poly = Poly(alpha.minimal_polynomial(x_sym), x_sym).monic()
                    h2 = (f == min_poly)
                else:
                    min_poly = Poly(minimal_polynomial(alpha, x_sym), x_sym).monic()
                    h2 = (f == min_poly)
    except Exception:
        h2 = False

    # Conclusion: The minimal polynomial of alpha^-1 over F is a0^-1 * x^n * f(1/x)
    try:
        if hasattr(alpha, 'inv'):
            try:
                alpha_inv = alpha.inv()
                is_invertible = True
            except Exception:
                is_invertible = False
        else:
            try:
                alpha_inv = 1 / alpha
                is_invertible = True
            except Exception:
                is_invertible = False
                
        if not is_invertible:
            neg_q = True
        else:
            a0 = f.nth(0)
            if a0 == 0:
                neg_q = True
            else:
                n = f.degree()
                f_expr = f.as_expr()
                f_1_x = f_expr.subs(x_sym, 1/x_sym)
                expected_expr = expand((1/a0) * (x_sym**n) * f_1_x)
                expected_poly = Poly(expected_expr, x_sym)
                
                if hasattr(alpha_inv, 'minimal_polynomial'):
                    actual_min_poly = Poly(alpha_inv.minimal_polynomial(x_sym), x_sym).monic()
                else:
                    actual_min_poly = Poly(minimal_polynomial(alpha_inv, x_sym), x_sym).monic()
                    
                neg_q = (expected_poly != actual_min_poly)
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: alpha is a non-zero element algebraic over F",
    "H_2: f(x) is the minimal polynomial of alpha over F",
    "¬Q: The minimal polynomial of alpha^-1 over F is not a0^-1 * x^n * f(1/x)"
]

N_HYP = 2
NEG_Q_INDEX = 2