import math
import sympy
from sympy import sqrt, I

# Top-level setup
# We provide sqrt and I for convenience if the witness uses sympy expressions.
# The verifier evaluates the conjecture in the ring Z[sqrt(d)] for d < 0.
# The default ring is Z[sqrt(-5)], a standard example of a non-UFD Schreier domain counterexample.

def mul(A, B, d):
    u, v = A
    x, y = B
    return (u*x + d*v*y, u*y + v*x)

def norm(A, d):
    u, v = A
    return u**2 - d * v**2

def divides(A, B, d):
    u, v = A
    x, y = B
    n = norm(A, d)
    if n == 0:
        return False
    s_num = u*x - d*v*y
    t_num = u*y - v*x
    return s_num % n == 0 and t_num % n == 0

def get_factors(A, d):
    n = norm(A, d)
    if n == 0 or n > 10**6:
        return []
    factors = []
    max_u = int(math.isqrt(n))
    max_v = int(math.isqrt(n // abs(d)))
    for u1 in range(-max_u - 1, max_u + 2):
        for v1 in range(-max_v - 1, max_v + 2):
            A1 = (u1, v1)
            n1 = norm(A1, d)
            if n1 == 0:
                continue
            if divides(A1, A, d):
                u, v = A
                s = (u1*u - d*v1*v) // n1
                t = (u1*v - v1*u) // n1
                A2 = (s, t)
                factors.append((A1, A2))
    return factors

def parse_element(expr):
    if isinstance(expr, tuple):
        if len(expr) == 2:
            return int(expr[0]), int(expr[1]), -5
        elif len(expr) == 3:
            return int(expr[0]), int(expr[1]), int(expr[2])
            
    expr = sympy.sympify(expr)
    re, im = expr.as_real_imag()
    
    if not re.is_Integer:
        re = sympy.simplify(re)
        if not re.is_Integer:
            raise ValueError("Real part must be an integer")
            
    u = int(re)
    
    if im == 0:
        return u, 0, -5
        
    im_sq = sympy.simplify(im**2)
    if not im_sq.is_Integer:
        raise ValueError("Only Z[sqrt(d)] is supported")
        
    num = int(im_sq)
    if num == 0:
        return u, 0, -5
        
    factors = sympy.factorint(num)
    v = 1
    abs_d = 1
    for p, exp in factors.items():
        v *= p**(exp // 2)
        abs_d *= p**(exp % 2)
        
    if bool(im < 0):
        v = -v
        
    return u, v, -abs_d

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can be a tuple (a, b, c) or (d, a, b, c), or a dict with these keys.
    Elements can be sympy expressions like `1 + sqrt(-5)` or tuples like `(u, v)`.
    """
    try:
        if isinstance(witness, dict):
            a_wit = witness['a']
            b_wit = witness['b']
            c_wit = witness['c']
            if 'd' in witness:
                witness = (witness['d'], a_wit, b_wit, c_wit)
            else:
                witness = (a_wit, b_wit, c_wit)
                
        if len(witness) == 4:
            d_wit, a_wit, b_wit, c_wit = witness
            a_parsed = parse_element(a_wit)
            b_parsed = parse_element(b_wit)
            c_parsed = parse_element(c_wit)
            d = int(d_wit)
            a = (a_parsed[0], a_parsed[1])
            b = (b_parsed[0], b_parsed[1])
            c = (c_parsed[0], c_parsed[1])
        elif len(witness) == 3:
            a_wit, b_wit, c_wit = witness
            a_parsed = parse_element(a_wit)
            b_parsed = parse_element(b_wit)
            c_parsed = parse_element(c_wit)
            
            ds = {x[2] for x in [a_parsed, b_parsed, c_parsed] if x[1] != 0}
            if len(ds) > 1:
                return [False, False, False]
            d = ds.pop() if ds else -5
            
            a = (a_parsed[0], a_parsed[1])
            b = (b_parsed[0], b_parsed[1])
            c = (c_parsed[0], c_parsed[1])
        else:
            return [False, False, False]
            
        if d >= 0:
            return [False, False, False]
            
        # H1: a, b, c are non-zero
        h1_ok = (a != (0, 0) and b != (0, 0) and c != (0, 0))
        
        # H2: a divides bc
        bc = mul(b, c, d)
        h2_ok = divides(a, bc, d)
        
        # neg_Q: there do NOT exist a1, a2 such that a = a1*a2, a1|b, a2|c
        factors = get_factors(a, d)
        if not factors:
            neg_q_ok = False
        else:
            exists = False
            for a1, a2 in factors:
                if divides(a1, b, d) and divides(a2, c, d):
                    exists = True
                    break
            neg_q_ok = not exists
            
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements in R",
    "H_2: a divides the product bc",
    "¬Q: There do not exist a_1, a_2 such that a = a_1 * a_2, a_1 | b, and a_2 | c"
]

N_HYP = 2
NEG_Q_INDEX = 2