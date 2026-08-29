import math
import sympy

# Top-level setup
Z = sympy.Symbol('Z')
ZZ = sympy.Symbol('ZZ')
QQ = sympy.Symbol('QQ')

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def get_n(expr):
    if isinstance(expr, (list, set, tuple)):
        return len(expr)
    if expr is sympy.S.Integers:
        return 0
    try:
        if expr == sympy.polys.domains.ZZ:
            return 0
    except Exception:
        pass
    if isinstance(expr, int):
        return abs(expr)
    if hasattr(expr, 'is_Integer') and expr.is_Integer:
        return abs(int(expr))
    if isinstance(expr, sympy.Expr):
        if expr in (Z, ZZ):
            return 0
        if len(expr.free_symbols) == 0:
            return abs(int(expr))
    if isinstance(expr, str):
        s = expr.strip()
        if s in ('Z', 'ZZ', 'Integers'):
            return 0
        return abs(int(s))
    return abs(int(expr))

def get_m(expr):
    if isinstance(expr, (list, set, tuple)):
        try:
            positives = [abs(int(e)) for e in expr if int(e) != 0]
            if positives:
                return min(positives)
            return 1
        except Exception:
            pass
            
    if isinstance(expr, int):
        return abs(expr)
    if hasattr(expr, 'is_Integer') and expr.is_Integer:
        return abs(int(expr))
    if isinstance(expr, sympy.Expr):
        if expr in (Z, ZZ):
            return 1
        free = expr.free_symbols
        if len(free) == 1:
            sym = list(free)[0]
            if sym.name in ('Z', 'ZZ'):
                coeff = expr.coeff(sym)
                if coeff != 0 and coeff.is_Integer:
                    return abs(int(coeff))
        if len(free) == 0:
            return abs(int(expr))
    if isinstance(expr, str):
        s = expr.strip()
        if s in ('Z', 'ZZ'):
            return 1
        if s.endswith('Z'):
            val = s[:-1]
            if val == '': return 1
            return abs(int(val))
        return abs(int(s))
    return abs(int(expr))

def get_x(expr):
    if isinstance(expr, int):
        return expr
    if hasattr(expr, 'is_Integer') and expr.is_Integer:
        return int(expr)
    if isinstance(expr, sympy.Expr):
        if len(expr.free_symbols) == 0:
            return int(expr)
    if isinstance(expr, str):
        return int(expr.strip())
    return int(expr)

def conditions(witness) -> list[bool]:
    """
    Expects a witness representing a ring R, an ideal I, and an element x.
    For finite rings Z/nZ, the witness can be a tuple (n, m, x) where:
      - n is the modulus of the ring (n=0 represents Z)
      - m is the modulus of the ideal (m divides n)
      - x is the element
    """
    try:
        if isinstance(witness, dict):
            n = get_n(witness.get('n', witness.get('R', 0)))
            m = get_m(witness.get('m', witness.get('I', 1)))
            x = get_x(witness.get('x', witness.get('elem', 0)))
        else:
            n = get_n(witness[0])
            m = get_m(witness[1])
            x = get_x(witness[2])
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a ring with identity and I is an ideal of R
    try:
        if n == 0:
            h1 = (m >= 2)
        else:
            h1 = (n >= 2 and m >= 2 and n % m == 0)
    except Exception:
        h1 = False
        
    # H2: x is an element of R
    try:
        h2 = isinstance(x, int)
    except Exception:
        h2 = False
        
    # H3: The image of x in R/I is a unit
    try:
        h3 = (math.gcd(x, m) == 1)
    except Exception:
        h3 = False
        
    # neg_Q: x is not a unit in R
    try:
        if n == 0:
            neg_q = (abs(x) != 1)
        else:
            neg_q = (math.gcd(x, n) != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity and I is an ideal of R",
    "H_2: x is an element of R",
    "H_3: The image of x in R/I is a unit",
    "¬Q: x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3