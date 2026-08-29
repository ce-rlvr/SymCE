import sympy as sp
from sympy.ntheory import divisors

# Top-level setup
w = sp.sqrt(-5)
Z_sqrt_minus_5 = "Z[sqrt(-5)]"

def get_quadratic_extension(exprs):
    bases = set()
    for expr in exprs:
        if hasattr(expr, 'atoms'):
            for atom in expr.atoms(sp.Pow):
                if atom.exp == sp.Half:
                    bases.add(atom.base)
            if sp.I in expr.atoms():
                bases.add(sp.S(-1))
    
    bases.discard(sp.S(1))
    
    if len(bases) == 0:
        return 1
    elif len(bases) == 1:
        return list(bases)[0]
    elif len(bases) == 2 and sp.S(-1) in bases:
        bases.discard(sp.S(-1))
        b = list(bases)[0]
        return -b
    return None

def parse_element(expr, D):
    if D == 1:
        return (sp.simplify(expr), sp.S(0))
    
    expr = sp.expand(expr)
    if D < 0:
        u = sp.re(expr)
        v = sp.im(expr) / sp.sqrt(-D)
    else:
        expr = sp.radsimp(expr)
        indep, dep = expr.as_independent(sp.sqrt(D))
        v = dep / sp.sqrt(D)
        u = indep
    return sp.simplify(u), sp.simplify(v)

def is_in_ring(expr, D):
    try:
        u, v = parse_element(expr, D)
        u_ok = u.is_integer or (u.is_Rational and u.q == 1)
        v_ok = v.is_integer or (v.is_Rational and v.q == 1)
        return bool(u_ok and v_ok)
    except Exception:
        return False

def norm(expr, D):
    u, v = parse_element(expr, D)
    return u**2 - D * v**2

def divides(divisor, dividend, D):
    if divisor == 0:
        return False
    try:
        quot = sp.simplify(dividend / divisor)
        return is_in_ring(quot, D)
    except Exception:
        return False

def are_coprime(a, b, D):
    try:
        Na = sp.Abs(norm(a, D))
        Nb = sp.Abs(norm(b, D))
        g = sp.gcd(Na, Nb)
        if g == 1:
            return True
        if D < 0:
            divs = divisors(g)
            for k in divs:
                if k == 1:
                    continue
                max_v = int((float(k) / float(-D))**0.5)
                for v in range(-max_v - 1, max_v + 2):
                    u2 = k + D * v**2
                    if u2 >= 0:
                        u = int(float(u2)**0.5)
                        if u**2 == u2:
                            d1 = u + v*sp.sqrt(D)
                            d2 = -u + v*sp.sqrt(D)
                            for d in [d1, d2]:
                                if divides(d, a, D) and divides(d, b, D):
                                    return False
            return True
        else:
            return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            a, b, c = witness
        else:
            return [False] * 5
            
        a = sp.sympify(a)
        b = sp.sympify(b)
        c = sp.sympify(c)
        
        D = get_quadratic_extension([a, b, c])
        if D is None:
            return [False] * 5
            
        h1 = is_in_ring(a, D) and is_in_ring(b, D) and is_in_ring(c, D) and a != 0 and b != 0 and c != 0
        h2 = are_coprime(a, b, D)
        h3 = divides(a, c, D)
        h4 = divides(b, c, D)
        
        ab = sp.expand(a * b)
        q_holds = divides(ab, c, D)
        neg_q = not q_holds
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements in R",
    "H_2: a and b are coprime",
    "H_3: a divides c in R",
    "H_4: b divides c in R",
    "¬Q: The product ab does not divide c in R"
]

N_HYP = 4
NEG_Q_INDEX = 4