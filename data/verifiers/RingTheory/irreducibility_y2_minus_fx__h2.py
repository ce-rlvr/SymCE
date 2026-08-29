import sympy
import math

x = sympy.Symbol('x')
y = sympy.Symbol('y')
QQ = sympy.QQ
ZZ = sympy.ZZ

def get_f_and_domain(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        domain, f = witness
        if isinstance(f, str):
            f = sympy.sympify(f)
        return f, domain
    elif hasattr(witness, 'domain') and hasattr(witness, 'as_expr'):
        return witness.as_expr(), witness.domain
    else:
        if isinstance(witness, str):
            witness = sympy.sympify(witness)
        return witness, None

def conditions(witness):
    # H1: F is a field of characteristic not equal to 2
    h1_ok = False
    try:
        f, domain = get_f_and_domain(witness)
        if domain is not None:
            if hasattr(domain, 'is_Field') and hasattr(domain, 'characteristic'):
                h1_ok = bool(domain.is_Field and domain.characteristic != 2)
            else:
                h1_ok = True
        else:
            h1_ok = True
    except Exception:
        h1_ok = False

    # H2: There does not exist a polynomial g(x) in F[x] such that f(x) is the square of g(x)
    h2_ok = False
    try:
        f, domain = get_f_and_domain(witness)
        if not hasattr(f, 'free_symbols'):
            f = sympy.sympify(f)
        free_syms = f.free_symbols
        
        if not free_syms.issubset({x}):
            h2_ok = True
        elif not f.is_polynomial(x):
            h2_ok = True
        else:
            if domain is not None:
                coeff, factors = sympy.factor_list(f, domain=domain)
            else:
                coeff, factors = sympy.factor_list(f)
                
            is_square = True
            for factor, mult in factors:
                if mult % 2 != 0:
                    is_square = False
                    break
            if is_square:
                if domain is not None and hasattr(domain, 'characteristic') and domain.characteristic > 0:
                    p = domain.characteristic
                    if p > 2:
                        try:
                            c_val = int(coeff) % p
                            if c_val != 0 and pow(c_val, (p - 1) // 2, p) != 1:
                                is_square = False
                        except Exception:
                            pass
                elif domain == sympy.RR:
                    try:
                        if float(coeff) < 0:
                            is_square = False
                    except Exception:
                        pass
                elif domain == sympy.CC:
                    pass
                else:
                    try:
                        c = sympy.Rational(coeff)
                        if c < 0:
                            is_square = False
                        else:
                            if math.isqrt(c.p)**2 != c.p or math.isqrt(c.q)**2 != c.q:
                                is_square = False
                    except Exception:
                        is_square = False
            h2_ok = not is_square
    except Exception:
        h2_ok = True

    # neg_Q: The polynomial y^2 - f(x) is NOT irreducible in F[x,y]
    neg_q_ok = False
    try:
        f, domain = get_f_and_domain(witness)
        if not hasattr(f, 'free_symbols'):
            f = sympy.sympify(f)
        expr = y**2 - f
        
        if not expr.is_polynomial(x, y):
            neg_q_ok = True
        else:
            if domain is not None:
                coeff, factors = sympy.factor_list(expr, domain=domain)
            else:
                coeff, factors = sympy.factor_list(expr)
            
            total_mult = sum(mult for fac, mult in factors)
            neg_q_ok = bool(total_mult != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: f is not the square of a polynomial g",
    "¬Q: y^2 - f is reducible or not a polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2