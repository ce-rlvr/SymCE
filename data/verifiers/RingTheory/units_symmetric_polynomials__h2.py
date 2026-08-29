import sympy
from sympy import expand, Poly
from sympy.ntheory import isprime
from sympy.abc import x, y, z

def is_zero_mod_m(expr, m):
    try:
        m = abs(int(m))
        if m == 1:
            return True
        expr = expand(expr)
        if expr == 0:
            return True
        if m == 0:
            return False
        
        free_syms = list(expr.free_symbols)
        if not free_syms:
            return int(expr) % m == 0
                
        p = Poly(expr, *free_syms, domain='ZZ')
        for coeff in p.coeffs():
            if int(coeff) % m != 0:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 3:
            u, v, xs = witness
            m = 0
        elif len(witness) == 4:
            u, v, xs, m = witness
        else:
            return [False, False]
        m_int = abs(int(m))
    except Exception:
        return [False, False]
        
    try:
        if m_int == 0:
            h1 = True
        else:
            h1 = isprime(m_int)
    except Exception:
        h1 = False
        
    try:
        u = sympy.sympify(u)
        v = sympy.sympify(v)
        xs = [sympy.sympify(var) for var in xs]
        
        all_syms = list(u.free_symbols | v.free_symbols)
        if all_syms:
            Poly(u, *all_syms)
            Poly(v, *all_syms)
            
        sym_u = True
        for i in range(len(xs) - 1):
            swapped = u.subs({xs[i]: xs[i+1], xs[i+1]: xs[i]})
            if not is_zero_mod_m(u - swapped, m_int):
                sym_u = False
                break
                
        sym_v = True
        for i in range(len(xs) - 1):
            swapped = v.subs({xs[i]: xs[i+1], xs[i+1]: xs[i]})
            if not is_zero_mod_m(v - swapped, m_int):
                sym_v = False
                break
                
        if not (sym_u and sym_v):
            neg_q = False
        else:
            if not is_zero_mod_m(u * v - 1, m_int):
                neg_q = False
            else:
                u_const = u.subs({var: 0 for var in xs})
                if is_zero_mod_m(u - u_const, m_int):
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The group of units of the symmetric polynomial ring is not exactly the group of units of R"
]

N_HYP = 1
NEG_Q_INDEX = 1