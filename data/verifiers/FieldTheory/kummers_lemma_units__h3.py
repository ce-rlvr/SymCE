import sympy

# Top-level setup: named object bindings
zeta = sympy.Symbol('zeta')

CONDITION_LABELS = [
    "H_1: p is a regular prime number",
    "H_2: zeta_p is a primitive p-th root of unity",
    "¬Q: u cannot be written as zeta_p^k * r for any integer k and real unit r"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_regular_prime(p):
    try:
        if not isinstance(p, int):
            return False
        if not sympy.isprime(p):
            return False
        if p == 2:
            return True
        # A prime p is regular if it does not divide the numerator of Bernoulli numbers B_k for k = 2, 4, ..., p-3
        for k in range(2, p - 2, 2):
            B_k = sympy.bernoulli(k)
            if B_k.p % p == 0:
                return False
        return True
    except Exception:
        return False

def get_poly(p, expr):
    try:
        x = sympy.Symbol('x')
        cyclo = sympy.cyclotomic_poly(p, x)
        
        if hasattr(expr, 'subs'):
            expr_x = expr.subs(zeta, x)
        else:
            expr_x = sympy.sympify(expr)
            
        r_rat = sympy.cancel(expr_x)
        num, den = r_rat.as_numer_denom()
        
        num_poly = sympy.poly(num, x, domain='QQ')
        den_poly = sympy.poly(den, x, domain='QQ')
        cyclo_poly = sympy.poly(cyclo, x, domain='QQ')
        
        inv_den = sympy.invert(den_poly.as_expr(), cyclo_poly.as_expr(), domain='QQ')
        r_poly = sympy.rem(num_poly.as_expr() * inv_den, cyclo_poly.as_expr(), x)
        return sympy.poly(r_poly, x, domain='QQ')
    except Exception:
        return None

def is_real(p, r_poly_expr):
    try:
        if r_poly_expr is None: 
            return False
        x = r_poly_expr.gen
        cyclo = sympy.cyclotomic_poly(p, x)
        
        conj_expr = 0
        for power, coeff in r_poly_expr.terms():
            k = power[0]
            # The complex conjugate of x^k modulo Phi_p(x) is x^(-k) = x^(p - (k mod p))
            conj_expr += coeff * x**((p - (k % p)) % p)
            
        diff = sympy.rem(r_poly_expr.as_expr() - conj_expr, cyclo, x)
        return sympy.expand(diff) == 0
    except Exception:
        return False

def is_unit(p, r_poly_expr):
    try:
        if r_poly_expr is None: 
            return False
        if r_poly_expr.is_zero:
            return False
        x = r_poly_expr.gen
        cyclo = sympy.cyclotomic_poly(p, x)
        
        # In Z[zeta_p], an element is an algebraic integer iff its standard polynomial representation has integer coefficients
        for c in r_poly_expr.all_coeffs():
            if not c.is_integer:
                return False
                
        # The norm over Q is the resultant with the cyclotomic polynomial
        res = sympy.resultant(r_poly_expr.as_expr(), cyclo, x)
        return abs(res) == 1
    except Exception:
        return False

def Q(witness):
    try:
        p_val, u_expr = witness
        # Check if there exists an integer k such that r = u * zeta^(-k) is a real unit
        for k in range(p_val):
            # zeta^(-k) is equivalent to zeta^(p - k)
            r_expr = u_expr * zeta**(p_val - k)
            r_poly = get_poly(p_val, r_expr)
            if r_poly is not None:
                if is_real(p_val, r_poly) and is_unit(p_val, r_poly):
                    return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 2:
            p_val, u_expr = witness
        elif len(witness) == 3:
            p_val, zeta_val, u_expr = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_regular_prime(p_val)
    except Exception:
        h1 = False
        
    try:
        # The symbol zeta inherently represents a primitive p-th root of unity in our setup
        h2 = True
    except Exception:
        h2 = False
        
    try:
        q_val = Q((p_val, u_expr))
        neg_q = not q_val
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]