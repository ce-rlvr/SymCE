import sympy as sp

# Top-level setup
x, y, z = sp.symbols('x y z')

def is_ufd(R):
    return R in ['Z', 'Q[x]', 'Z[x]', 'R[x]', 'C[x]']

def in_ring(val, R):
    try:
        val = sp.sympify(val)
        if R == 'Z':
            return val.is_Integer
        
        if R == 'Z[x]': dom = sp.ZZ
        elif R == 'Q[x]': dom = sp.QQ
        elif R == 'R[x]': dom = sp.RR
        elif R == 'C[x]': dom = sp.CC
        else: return False
        
        syms = val.free_symbols
        if len(syms) > 1:
            return False
        sym = list(syms)[0] if syms else x
            
        p = sp.Poly(val, sym)
        return dom.unify(p.domain) == dom
    except Exception:
        return False

def divides(x_val, y_val, R):
    try:
        x_val = sp.sympify(x_val)
        y_val = sp.sympify(y_val)
        if x_val == 0:
            return y_val == 0
        if R == 'Z':
            return y_val % x_val == 0
            
        if R == 'Z[x]': dom = sp.ZZ
        elif R == 'Q[x]': dom = sp.QQ
        elif R == 'R[x]': dom = sp.RR
        elif R == 'C[x]': dom = sp.CC
        else: dom = sp.QQ
        
        if x_val.is_constant() and y_val.is_constant():
            if R == 'Z[x]':
                return y_val % x_val == 0
            else:
                return True
                
        syms = x_val.free_symbols | y_val.free_symbols
        if len(syms) > 1:
            return False
        sym = list(syms)[0] if syms else x
        
        q, r = sp.div(y_val, x_val, sym, domain=dom)
        return r == 0
    except Exception:
        return False

def is_gcd(d, a, b, R):
    try:
        if not (divides(d, a, R) and divides(d, b, R)):
            return False
            
        a_val = sp.sympify(a)
        b_val = sp.sympify(b)
        if R == 'Z':
            g = sp.gcd(a_val, b_val)
        else:
            if R == 'Z[x]': dom = sp.ZZ
            elif R == 'Q[x]': dom = sp.QQ
            elif R == 'R[x]': dom = sp.RR
            elif R == 'C[x]': dom = sp.CC
            else: dom = sp.QQ
            
            g = sp.gcd(a_val, b_val, domain=dom)
            
        return divides(g, d, R)
    except Exception:
        return False

def are_associates(d1, d2, R):
    return divides(d1, d2, R) and divides(d2, d1, R)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            a = witness.get('a')
            b = witness.get('b')
            d1 = witness.get('d1')
            d2 = witness.get('d2')
        elif isinstance(witness, (list, tuple)) and len(witness) == 5:
            R, a, b, d1, d2 = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(is_ufd(R))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(in_ring(a, R) and in_ring(b, R))
    except Exception:
        h2 = False
        
    try:
        h3 = bool(in_ring(d2, R) and is_gcd(d2, a, b, R))
    except Exception:
        h3 = False
        
    try:
        if not in_ring(d1, R):
            neg_q = True
        else:
            neg_q = not are_associates(d1, d2, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are elements of R",
    "H_3: d2 is a greatest common divisor of a and b",
    "¬Q: There does not exist a unit u in R such that d1 = u * d2"
]

N_HYP = 3
NEG_Q_INDEX = 3