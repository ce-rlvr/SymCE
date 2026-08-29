import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_prime(F):
    if isinstance(F, int) and sympy.isprime(F):
        return F
    if hasattr(F, 'mod') and sympy.isprime(F.mod):
        return F.mod
    if hasattr(F, 'p') and sympy.isprime(F.p):
        return F.p
    return None

def get_F_str(F):
    if F in ['Q', 'R', 'C']: return F
    s = str(F)
    if s in ['QQ', 'Rationals']: return 'Q'
    if s in ['RR', 'Reals']: return 'R'
    if s in ['CC', 'Complexes']: return 'C'
    return F

def is_field(F):
    if F in ['Q', 'R', 'C']: return True
    if str(F) in ['QQ', 'RR', 'CC', 'Reals', 'Rationals', 'Complexes']: return True
    if get_prime(F) is not None: return True
    return False

def in_field(val, F):
    F = get_F_str(F)
    try:
        v = sympy.sympify(val)
        if F == 'Q': return v.is_rational
        if F == 'R': return v.is_real
        if F == 'C': return v.is_complex
        p = get_prime(F)
        if p is not None: return v.is_integer
    except Exception:
        return False
    return False

def extract_scalar(val):
    if hasattr(val, 'shape') and val.shape == (1, 1):
        return val[0, 0]
    if isinstance(val, list) and len(val) == 1 and isinstance(val[0], list) and len(val[0]) == 1:
        return val[0][0]
    return val

def has_square_ratio(x, y, F):
    F = get_F_str(F)
    try:
        x = sympy.sympify(x)
        y = sympy.sympify(y)
    except Exception:
        return False
        
    if x == 0 and y == 0: return True
    if x == 0 or y == 0: return False
    
    if F == 'Q':
        try:
            ratio = sympy.Rational(x) / sympy.Rational(y)
            if ratio < 0: return False
            num = ratio.p
            den = ratio.q
            return sympy.integer_nthroot(num, 2)[1] and sympy.integer_nthroot(den, 2)[1]
        except Exception:
            return False
    if F == 'R':
        try:
            return bool((x * y) > 0)
        except Exception:
            return False
    if F == 'C':
        return True
        
    p = get_prime(F)
    if p is not None:
        try:
            x = int(x) % p
            y = int(y) % p
            if x == 0 and y == 0: return True
            if x == 0 or y == 0: return False
            if p == 2: return True
            ratio = (x * pow(y, p - 2, p)) % p
            return sympy.legendre_symbol(ratio, p) == 1 or ratio == 1
        except Exception:
            return False
            
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            B_V = extract_scalar(witness.get('B_V'))
            B_W = extract_scalar(witness.get('B_W'))
            a = extract_scalar(witness.get('a'))
            b = extract_scalar(witness.get('b'))
        else:
            F = getattr(witness, 'F', None)
            B_V = extract_scalar(getattr(witness, 'B_V', None))
            B_W = extract_scalar(getattr(witness, 'B_W', None))
            a = extract_scalar(getattr(witness, 'a', None))
            b = extract_scalar(getattr(witness, 'b', None))
            
        h1 = is_field(F) and in_field(B_V, F) and in_field(B_W, F) and in_field(a, F) and in_field(b, F)
        
        h2 = (sympy.sympify(B_V) != 0) and (sympy.sympify(B_W) != 0)
        
        P = has_square_ratio(B_V, B_W, F)
        Q = has_square_ratio(a, b, F)
        
        neg_q = (P != Q)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V and W are one-dimensional vector spaces over a field F",
    "H_2: B_V and B_W are non-degenerate symmetric bilinear forms on V and W, respectively",
    "¬Q: The equivalence ((V, B_V) and (W, B_W) are isometric iff exists c != 0 such that a = c^2 b) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2