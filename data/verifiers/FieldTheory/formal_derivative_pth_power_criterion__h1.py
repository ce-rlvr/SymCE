import sympy
from sympy.ntheory import factorint

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x')
t = sympy.Symbol('t')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

def guess_p(f, x_sym):
    """Attempt to infer the characteristic p from the derivative of f."""
    try:
        deriv = sympy.diff(f, x_sym)
        if deriv == 0:
            return None
        d = deriv.as_coefficients_dict()
        g = 0
        for term, coeff in d.items():
            if coeff.is_Integer:
                g = sympy.gcd(g, abs(int(coeff)))
            else:
                return None
        if g > 1:
            factors = factorint(g)
            if factors:
                return max(factors.keys())
    except Exception:
        pass
    return None

def parse_witness(witness, x_sym):
    p = None
    f = None
    if isinstance(witness, dict):
        p = witness.get('p')
        f = witness.get('f')
        if f is None and 'polynomial' in witness:
            f = witness['polynomial']
    elif isinstance(witness, tuple):
        if len(witness) == 2:
            if isinstance(witness[0], int):
                p, f = witness
            elif isinstance(witness[1], int):
                f, p = witness
            else:
                f = witness[1]
        elif len(witness) == 3:
            if isinstance(witness[0], int):
                p = witness[0]
                f = witness[2]
    else:
        f = witness

    if hasattr(f, 'domain') and hasattr(f.domain, 'char'):
        if p is None or p == 0:
            p = f.domain.char
            
    if hasattr(f, 'as_expr'):
        f = f.as_expr()
        
    if isinstance(f, str):
        try:
            f = sympy.sympify(f)
        except Exception:
            pass
            
    if p is not None:
        try:
            p = int(p)
        except Exception:
            pass

    if p is None and f is not None:
        p = guess_p(f, x_sym)
        
    return p, f

def reduce_mod_p(expr, p):
    expr = sympy.expand(expr)
    if expr == 0:
        return 0
    try:
        d = expr.as_coefficients_dict()
        res = 0
        for term, coeff in d.items():
            if coeff.is_Rational:
                num, den = coeff.p, coeff.q
                if den % p != 0:
                    c = (int(num) * pow(int(den), -1, int(p))) % int(p)
                    res += c * term
                else:
                    res += coeff * term
            else:
                res += coeff * term
        return res
    except Exception:
        return expr

def is_deriv_zero(f, x_sym, p):
    try:
        deriv = sympy.diff(f, x_sym)
        deriv_mod = reduce_mod_p(deriv, p)
        return deriv_mod == 0
    except Exception:
        return False

def is_pth_power_mod_p(f, p):
    try:
        f_mod = reduce_mod_p(f, p)
        if f_mod == 0:
            return True
        poly = sympy.Poly(f_mod, x)
        for monom in poly.monoms():
            if monom[0] % p != 0:
                return False
        for coeff in poly.coeffs():
            if coeff.is_Integer or coeff.is_Rational:
                continue
            coeff_dict = coeff.as_coefficients_dict()
            for term, c in coeff_dict.items():
                if term == 1:
                    continue
                powers = term.as_powers_dict()
                for var, exp in powers.items():
                    if exp % p != 0:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    p, f = parse_witness(witness, x)
    
    if p is None or p <= 1 or f is None:
        return [False, False, False]
        
    # H_1: f is a polynomial over F_q
    try:
        sympy.Poly(f, x)
        h1 = True
    except Exception:
        h1 = False
        
    # H_2: The formal derivative of f is identically the zero polynomial
    try:
        h2 = is_deriv_zero(f, x, p)
    except Exception:
        h2 = False
        
    # ¬Q: There does not exist a polynomial g over F_q such that f = g^p
    try:
        neg_q = not is_pth_power_mod_p(f, p)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over F_q",
    "H_2: The formal derivative of f is identically the zero polynomial",
    "not Q: There does not exist a polynomial g over F_q such that f = g^p"
]

N_HYP = 2
NEG_Q_INDEX = 2