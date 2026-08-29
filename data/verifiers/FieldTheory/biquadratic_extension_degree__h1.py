import sympy
from sympy import cancel, Poly, factor_list, diff, sympify, isprime
from sympy.abc import t, u, v, x, y, z

def is_square(expr, p):
    try:
        expr = cancel(expr)
        num, den = expr.as_numer_denom()
        dom = 'GF(%d)' % p
        num_poly = Poly(num, domain=dom)
        den_poly = Poly(den, domain=dom)
        
        if den_poly.is_zero:
            return False
            
        if num_poly.is_zero:
            return True
            
        num_fac = factor_list(num_poly)
        den_fac = factor_list(den_poly)
        
        c_num = int(num_fac[0]) % p
        c_den = int(den_fac[0]) % p
        
        if c_den == 0:
            return False
            
        c = (c_num * pow(c_den, p-2, p)) % p
        
        is_c_square = False
        for i in range(p):
            if (i*i) % p == c:
                is_c_square = True
                break
        if not is_c_square:
            return False
            
        for base, exp in num_fac[1]:
            if exp % 2 != 0:
                return False
        for base, exp in den_fac[1]:
            if exp % 2 != 0:
                return False
                
        return True
    except Exception:
        return False

def check_neg_Q(p, a, b):
    if p != 2:
        return False
        
    try:
        syms = list(a.free_symbols | b.free_symbols)
        if not syms:
            return True
            
        dom = 'GF(2)'
        y_sq = None
        for s in syms:
            try:
                db = Poly(diff(b, s), domain=dom).as_expr()
            except Exception:
                db = 0
            if db != 0:
                try:
                    da = Poly(diff(a, s), domain=dom).as_expr()
                    y_sq_raw = cancel(da / db)
                    num, den = y_sq_raw.as_numer_denom()
                    num = Poly(num, domain=dom).as_expr()
                    den = Poly(den, domain=dom).as_expr()
                    if den == 0:
                        continue
                    y_sq = cancel(num / den)
                    break
                except Exception:
                    continue
                    
        if y_sq is None:
            return True
            
        for s in syms:
            try:
                da = Poly(diff(a, s), domain=dom).as_expr()
                db = Poly(diff(b, s), domain=dom).as_expr()
                diff_deriv = cancel(da - y_sq * db)
                num, den = diff_deriv.as_numer_denom()
                if not Poly(num, domain=dom).is_zero:
                    return False
            except Exception:
                return False
                
        if not is_square(y_sq, 2):
            return False
            
        try:
            x_sq_raw = a - y_sq * b
            num, den = x_sq_raw.as_numer_denom()
            num = Poly(num, domain=dom).as_expr()
            den = Poly(den, domain=dom).as_expr()
            if den == 0:
                return False
            x_sq = cancel(num / den)
        except Exception:
            return False
            
        if not is_square(x_sq, 2):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        p, a, b = witness
    except Exception:
        return [False] * 5
        
    try:
        p = int(p)
        a = sympify(a)
        b = sympify(b)
        if not isprime(p):
            h1 = False
        else:
            dom = 'GF(%d)' % p
            a_num, a_den = cancel(a).as_numer_denom()
            b_num, b_den = cancel(b).as_numer_denom()
            if Poly(a_den, domain=dom).is_zero or Poly(b_den, domain=dom).is_zero:
                h1 = False
            else:
                Poly(a_num, domain=dom)
                Poly(b_num, domain=dom)
                h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = not is_square(a, p)
    except Exception:
        h2 = False
        
    try:
        h3 = not is_square(b, p)
    except Exception:
        h3 = False
        
    try:
        h4 = not is_square(a * b, p)
    except Exception:
        h4 = False
        
    try:
        neg_q = check_neg_Q(p, a, b)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of F",
    "H_2: a is not the square of any element in F",
    "H_3: b is not the square of any element in F",
    "H_4: The product ab is not the square of any element in F",
    "¬Q: The degree of the field extension F(sqrt(a), sqrt(b)) over F is not exactly 4"
]

N_HYP = 4
NEG_Q_INDEX = 4