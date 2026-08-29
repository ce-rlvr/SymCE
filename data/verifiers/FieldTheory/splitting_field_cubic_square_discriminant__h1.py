import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Symbol, Poly, GF

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    if isinstance(witness, str):
        witness = sympy.sympify(witness)
    
    if isinstance(witness, sympy.Poly):
        expr = witness.as_expr()
        x = witness.gen
        domain = witness.domain
        if domain.is_FiniteField:
            p = domain.char
            t = None
        elif hasattr(domain, 'char'):
            p = domain.char
            symbols = expr.free_symbols - {x}
            t = list(symbols)[0] if symbols else None
        else:
            p = 0
            symbols = expr.free_symbols - {x}
            t = list(symbols)[0] if symbols else None
        return expr, x, t, p
        
    if isinstance(witness, tuple):
        witness = list(witness)
        if isinstance(witness[0], str):
            witness[0] = sympy.sympify(witness[0])
        witness = tuple(witness)
        
        if len(witness) == 2:
            expr, p = witness
            symbols = list(expr.free_symbols)
            if len(symbols) == 1:
                x = symbols[0]
                t = None
            else:
                x = sympy.Symbol('x') if sympy.Symbol('x') in symbols else symbols[0]
                t = [s for s in symbols if s != x][0]
            return expr, x, t, p
        elif len(witness) == 3:
            expr, x, p = witness
            symbols = expr.free_symbols - {x}
            t = list(symbols)[0] if symbols else None
            return expr, x, t, p
        elif len(witness) == 4:
            return witness

    expr = witness
    symbols = list(expr.free_symbols)
    x = sympy.Symbol('x') if sympy.Symbol('x') in symbols else symbols[0]
    t = [s for s in symbols if s != x][0] if len(symbols) > 1 else None
    return expr, x, t, 2

def reduce_mod_p(expr, p):
    if p == 0:
        return sympy.expand(expr)
    expr = sympy.expand(expr)
    if expr.free_symbols:
        try:
            poly = sympy.Poly(expr, *expr.free_symbols)
            reduced_dict = {monom: c % p for monom, c in poly.terms()}
            return sympy.Poly(reduced_dict, *expr.free_symbols).as_expr()
        except Exception:
            return expr
    else:
        try:
            return sympy.Integer(int(expr) % p)
        except Exception:
            return expr

def get_coeffs(expr, x, t, p):
    poly = sympy.Poly(expr, x)
    if poly.degree() != 3:
        return None
    coeffs = poly.all_coeffs()
    return [reduce_mod_p(c, p) for c in coeffs]

def normalize_coeffs(coeffs, p):
    a, b, c, d = coeffs
    if a == 1:
        return coeffs
    if a == 0:
        return None
    if hasattr(a, 'free_symbols') and a.free_symbols:
        return None
    if p > 0:
        inv_a = pow(int(a), p-2, p)
        return [sympy.Integer(1), reduce_mod_p(b*inv_a, p), reduce_mod_p(c*inv_a, p), reduce_mod_p(d*inv_a, p)]
    else:
        return [sympy.Integer(1), b/a, c/a, d/a]

def get_divisors(d, t, p):
    if d == 0:
        return [sympy.Integer(0)]
    if t is None or not d.has(t):
        if p > 0:
            return [sympy.Integer(k) for k in range(1, p)]
        else:
            return []
    
    if p > 0:
        factors = sympy.factor_list(d, modulus=p)
        divs = [sympy.Integer(1)]
        for f, m in factors[1]:
            new_divs = []
            for i in range(m + 1):
                for div in divs:
                    new_divs.append(reduce_mod_p(div * (f**i), p))
            divs = new_divs
        all_divs = []
        for div in divs:
            for c in range(1, p):
                all_divs.append(reduce_mod_p(div * c, p))
        return all_divs
    else:
        return []

def is_irreducible(coeffs, t, p):
    a, b, c, d = coeffs
    if p == 0:
        x_sym = sympy.Symbol('x')
        expr = a*x_sym**3 + b*x_sym**2 + c*x_sym + d
        return sympy.factor(expr) == expr
    
    if t is None:
        for root in range(p):
            val = root**3 + b*root**2 + c*root + d
            if val % p == 0:
                return False
        return True
    else:
        divs = get_divisors(d, t, p)
        for root in divs:
            val = root**3 + b*root**2 + c*root + d
            if reduce_mod_p(val, p) == 0:
                return False
        return True

def get_discriminant(a, b, c, d, p):
    D = 18*a*b*c*d - 4*b**3*d + b**2*c**2 - 4*a*c**3 - 27*a**2*d**2
    return reduce_mod_p(D, p)

def is_square(D, t, p):
    D = reduce_mod_p(D, p)
    if D == 0:
        return True
    if t is None or not D.has(t):
        if p == 0:
            from sympy import sqrt
            return sqrt(D).is_Rational
        else:
            for k in range(p):
                if (k**2) % p == int(D):
                    return True
            return False
    else:
        if p == 0:
            factors = sympy.factor_list(D)
            if not is_square(factors[0], None, 0):
                return False
            for f, m in factors[1]:
                if m % 2 != 0:
                    return False
            return True
        elif p == 2:
            poly = sympy.Poly(D, t)
            for monom, c in poly.terms():
                if monom[0] % 2 != 0:
                    return False
            return True
        else:
            factors = sympy.factor_list(D, modulus=p)
            if not is_square(factors[0], None, p):
                return False
            for f, m in factors[1]:
                if m % 2 != 0:
                    return False
            return True

def splitting_field_degree_is_3(coeffs, t, p):
    a, b, c, d = coeffs
    if p == 2:
        if b == 0:
            return False
        else:
            if c == 0:
                return True
            divs = get_divisors(c, t, p)
            for A in divs:
                if reduce_mod_p(A**2 + b*A + c, p) == 0:
                    return True
            return False
    elif p == 3:
        return True
    else:
        D = get_discriminant(a, b, c, d, p)
        return is_square(D, t, p)

def conditions(witness):
    try:
        expr, x, t, p = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        coeffs = get_coeffs(expr, x, t, p)
        norm_coeffs = normalize_coeffs(coeffs, p) if coeffs else None
    except Exception:
        norm_coeffs = None

    try:
        H1 = is_irreducible(norm_coeffs, t, p) if norm_coeffs else False
    except Exception:
        H1 = False
        
    try:
        if norm_coeffs:
            a, b, c, d = norm_coeffs
            D = get_discriminant(a, b, c, d, p)
            H2 = is_square(D, t, p)
        else:
            H2 = False
    except Exception:
        H2 = False
        
    try:
        if norm_coeffs:
            deg_is_3 = splitting_field_degree_is_3(norm_coeffs, t, p)
            neg_Q = not deg_is_3
        else:
            neg_Q = False
    except Exception:
        neg_Q = False
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial of degree 3 over F",
    "H_2: The discriminant of f(x) is a perfect square in F",
    "¬Q: The degree of the splitting field of f(x) over F is not exactly 3"
]

N_HYP = 2
NEG_Q_INDEX = 2