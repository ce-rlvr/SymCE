import sympy as sp

# Top-level setup
x, y, z, t = sp.symbols('x y z t')

def is_int(val):
    return isinstance(val, int) or (hasattr(val, 'is_Integer') and val.is_Integer)

def parse_witness(witness):
    if not isinstance(witness, (tuple, list)):
        return None, None, None
    
    if len(witness) == 3:
        if is_int(witness[2]):
            a, b, p = witness
        elif is_int(witness[0]):
            p, a, b = witness
        elif hasattr(witness[0], 'characteristic'):
            p = witness[0].characteristic
            a, b = witness[1], witness[2]
        elif str(witness[0]) == 'GF(2)':
            p = 2
            a, b = witness[1], witness[2]
        else:
            a, b, p = witness
    elif len(witness) == 2:
        a, b = witness
        p = 0
        if hasattr(a, 'domain') and hasattr(a.domain, 'characteristic'):
            p = a.domain.characteristic
    else:
        return None, None, None
    
    try:
        p = int(p)
    except Exception:
        p = 0
        
    return a, b, p

def is_square_poly(poly_expr, p):
    try:
        poly_expr = sp.sympify(poly_expr)
        poly_expr = sp.expand(poly_expr)
        
        try:
            poly_expr = sp.Poly(poly_expr, domain=sp.GF(p)).as_expr()
        except Exception:
            pass
            
        if poly_expr == 0:
            return True
            
        if poly_expr.is_number:
            if poly_expr.is_Rational and not poly_expr.is_Integer:
                num, den = poly_expr.as_numer_denom()
                val = (int(num) * pow(int(den), p-2, p)) % p
            else:
                val = int(poly_expr) % p
            return any((i*i)%p == val for i in range(p))
            
        f = sp.factor(poly_expr, modulus=p)
        if f.is_Pow:
            base, exp = f.args
            return exp % 2 == 0
        elif f.is_Mul:
            for arg in f.args:
                if arg.is_number:
                    if arg.is_Rational and not arg.is_Integer:
                        num, den = arg.as_numer_denom()
                        val = (int(num) * pow(int(den), p-2, p)) % p
                    else:
                        val = int(arg) % p
                    if not any((i*i)%p == val for i in range(p)):
                        return False
                elif arg.is_Pow:
                    base, exp = arg.args
                    if exp % 2 != 0:
                        return False
                else:
                    return False
            return True
        else:
            return False
    except Exception:
        return False

def is_square_rat(expr, p):
    try:
        expr = sp.sympify(expr)
        if p == 0:
            if expr.is_number:
                return bool(sp.sqrt(expr).is_rational)
            f = sp.factor(expr)
            if f.is_Pow:
                return f.args[1] % 2 == 0
            elif f.is_Mul:
                for arg in f.args:
                    if arg.is_number:
                        if not sp.sqrt(arg).is_rational:
                            return False
                    elif arg.is_Pow:
                        if arg.args[1] % 2 != 0:
                            return False
                    else:
                        return False
                return True
            else:
                return False
        else:
            expr = sp.cancel(expr)
            num, den = expr.as_numer_denom()
            return is_square_poly(num, p) and is_square_poly(den, p)
    except Exception:
        return False

def conditions(witness):
    a, b, p = parse_witness(witness)
    if a is None:
        return [False] * 5
    
    try:
        if isinstance(a, sp.Poly):
            a = a.as_expr()
        else:
            a = sp.sympify(a)
            
        if isinstance(b, sp.Poly):
            b = b.as_expr()
        else:
            b = sp.sympify(b)
    except Exception:
        return [False] * 5

    try:
        # H1: a and b are elements of F
        h1 = True
        
        # H2: a is not a square in F
        try:
            h2 = not is_square_rat(a, p)
        except Exception:
            h2 = False
            
        # H3: b is not a square in F
        try:
            h3 = not is_square_rat(b, p)
        except Exception:
            h3 = False
            
        # H4: ab is not a square in F
        try:
            h4 = not is_square_rat(a * b, p)
        except Exception:
            h4 = False
            
        # neg_Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2
        # The conclusion is true in all fields of characteristic != 2.
        # In characteristic 2, the minimal polynomial has degree <= 2, so it cannot be the degree 4 polynomial.
        try:
            neg_q = (p == 2)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: a and b are elements of F",
    "H_2: a is not a square in F",
    "H_3: b is not a square in F",
    "H_4: ab is not a square in F",
    "¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2"
]

N_HYP = 4
NEG_Q_INDEX = 4