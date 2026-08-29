import sympy
from sympy import Symbol, Interval, S, diff, limit, sin, cos, exp, log, sqrt, pi, oo
from sympy.calculus.util import continuous_domain, function_range, periodicity

x = Symbol('x', real=True)

def is_finite_real_limit(L):
    try:
        from sympy import AccumBounds
        if L.has(AccumBounds):
            return False
        return bool(L.is_number and L.is_finite and L.is_real)
    except Exception:
        return False

def check_limit_exists_and_finite(f, x_var, pt, is_right):
    try:
        if pt is S.Infinity or pt is S.NegativeInfinity:
            L = limit(f, x_var, pt)
        else:
            dir = '+' if is_right else '-'
            L = limit(f, x_var, pt, dir=dir)
        return is_finite_real_limit(L)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            f, x_var, a, b = witness
            f = S(f)
            x_var = S(x_var)
            a = S(a)
            b = S(b)
        elif len(witness) == 3:
            f, a, b = witness
            f = S(f)
            a = S(a)
            b = S(b)
            free = f.free_symbols
            if len(free) == 1:
                x_var = list(free)[0]
            else:
                x_var = Symbol('x', real=True)
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    h1 = False
    try:
        domain = continuous_domain(f, x_var, Interval.open(a, b))
        is_cont = (domain == Interval.open(a, b))
        
        if is_cont:
            is_poly_deg_1 = False
            try:
                if f.is_polynomial(x_var):
                    poly = f.as_poly(x_var)
                    if poly is not None and poly.degree() <= 1:
                        is_poly_deg_1 = True
            except Exception:
                pass

            if is_poly_deg_1:
                h1 = True
            else:
                df = diff(f, x_var)
                if df.is_constant():
                    h1 = True
                else:
                    try:
                        frange = function_range(df, x_var, Interval.open(a, b))
                        if frange.inf > -S.Infinity and frange.sup < S.Infinity:
                            h1 = True
                    except Exception:
                        pass
                        
                if not h1:
                    try:
                        if periodicity(f, x_var) is not None:
                            h1 = True
                    except Exception:
                        pass
                        
                if not h1:
                    if check_limit_exists_and_finite(f, x_var, a, True) and check_limit_exists_and_finite(f, x_var, b, False):
                        h1 = True
                        
                if not h1:
                    c = S(0)
                    if a.is_finite and b.is_finite:
                        c = (a + b) / 2
                    elif a.is_finite:
                        c = a + 1
                    elif b.is_finite:
                        c = b - 1
                    
                    try:
                        is_valid_c = bool(a < c) and bool(c < b)
                    except Exception:
                        is_valid_c = False
                        
                    if is_valid_c:
                        ok1 = False
                        if a.is_finite:
                            ok1 = check_limit_exists_and_finite(f, x_var, a, True) and check_limit_exists_and_finite(f, x_var, c, False)
                        else:
                            try:
                                fr1 = function_range(df, x_var, Interval.open(a, c))
                                if fr1.inf > -S.Infinity and fr1.sup < S.Infinity:
                                    ok1 = True
                            except Exception:
                                pass
                                
                        ok2 = False
                        if b.is_finite:
                            ok2 = check_limit_exists_and_finite(f, x_var, c, True) and check_limit_exists_and_finite(f, x_var, b, False)
                        else:
                            try:
                                fr2 = function_range(df, x_var, Interval.open(c, b))
                                if fr2.inf > -S.Infinity and fr2.sup < S.Infinity:
                                    ok2 = True
                            except Exception:
                                pass
                                
                        if ok1 and ok2:
                            h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        domain = continuous_domain(f, x_var, Interval.open(a, b))
        is_cont = (domain == Interval.open(a, b))
        if not is_cont:
            neg_q = True
        elif a is S.NegativeInfinity or a is S.Infinity or b is S.NegativeInfinity or b is S.Infinity:
            neg_q = True
        elif not (a.is_finite and b.is_finite):
            neg_q = True
        else:
            L_a_ok = check_limit_exists_and_finite(f, x_var, a, True)
            L_b_ok = check_limit_exists_and_finite(f, x_var, b, False)
            if not (L_a_ok and L_b_ok):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: f is uniformly continuous on the open interval", "not Q: f does not have a unique continuous extension to the closed interval"]

N_HYP = 1
NEG_Q_INDEX = 1