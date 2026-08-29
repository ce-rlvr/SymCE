import sympy
from sympy import sqrt
import math

# Top-level setup for standard groups and rings
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

from sympy.matrices import eye, zeros
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Helper functions for arithmetic in Z[sqrt(d)]
def is_zero(u):
    return u[0] == 0 and u[1] == 0

def norm(u, d):
    return u[0]**2 - d * u[1]**2

def add(u, v):
    return (u[0] + v[0], u[1] + v[1])

def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])

def mul(u, v, d):
    return (u[0]*v[0] + d*u[1]*v[1], u[0]*v[1] + u[1]*v[0])

def divides(u, v, d):
    if is_zero(u):
        return is_zero(v)
    Nu = norm(u, d)
    if Nu == 0:
        return False
    conj_u = (u[0], -u[1])
    prod = mul(v, conj_u, d)
    return prod[0] % Nu == 0 and prod[1] % Nu == 0

def exact_div(v, u, d):
    Nu = norm(u, d)
    conj_u = (u[0], -u[1])
    prod = mul(v, conj_u, d)
    return (prod[0] // Nu, prod[1] // Nu)

def get_all_divisors(u, d):
    if is_zero(u):
        return set()
    Nu = norm(u, d)
    divs = set()
    max_x = int(math.isqrt(abs(Nu))) + 1
    max_y = int(math.isqrt(abs(Nu // abs(d)))) + 1 if d < 0 else 0
    for x in range(-max_x - 1, max_x + 2):
        for y in range(-max_y - 1, max_y + 2):
            v = (x, y)
            if not is_zero(v):
                Nv = norm(v, d)
                if Nv != 0 and Nu % Nv == 0:
                    if divides(v, u, d):
                        divs.add(v)
    return divs

def get_gcds(a, b, d):
    divs_a = get_all_divisors(a, d)
    divs_b = get_all_divisors(b, d)
    common_divs = divs_a.intersection(divs_b)
    
    gcds = set()
    for g in common_divs:
        is_gcd = True
        for cd in common_divs:
            if not divides(cd, g, d):
                is_gcd = False
                break
        if is_gcd:
            gcds.add(g)
    return gcds

def find_r(a, b, g, d):
    ag = exact_div(a, g, d)
    for x in range(-50, 51):
        for y in range(-50, 51):
            r = (x, y)
            if is_zero(r):
                continue
            rb = mul(r, b, d)
            if divides(a, rb, d):
                if not divides(ag, r, d):
                    return r
    return None

def parse_witness(witness):
    if not isinstance(witness, (tuple, list)):
        raise ValueError("Witness must be a tuple or list")
        
    if len(witness) >= 4 and isinstance(witness[0], int) and witness[0] < 0:
        d = witness[0]
        a = witness[1]
        b = witness[2]
        r = witness[3]
        if isinstance(a, tuple) and isinstance(b, tuple) and isinstance(r, tuple):
            return d, a, b, r

    if len(witness) >= 3 and isinstance(witness[0], int) and witness[0] < 0:
        d = witness[0]
        a = witness[1]
        b = witness[2]
        if isinstance(a, tuple) and isinstance(b, tuple):
            return d, a, b, None

    exprs = []
    for item in witness:
        if isinstance(item, (sympy.Expr, int)):
            exprs.append(item)
            
    if len(exprs) >= 2:
        if len(exprs) >= 3:
            a_expr = exprs[-3]
            b_expr = exprs[-2]
            r_expr = exprs[-1]
        else:
            a_expr = exprs[-2]
            b_expr = exprs[-1]
            r_expr = None
            
        d = None
        for expr in [a_expr, b_expr]:
            if isinstance(expr, sympy.Expr):
                for arg in expr.atoms(sympy.Pow):
                    if arg.exp == sympy.Rational(1, 2):
                        base = arg.base
                        if base.is_Integer and base < 0:
                            d = int(base)
                            break
            if d is not None:
                break
                
        if d is None:
            d = -5
            
        def to_tuple(expr, d):
            if expr is None:
                return None
            if isinstance(expr, tuple):
                return expr
            if isinstance(expr, int):
                return (expr, 0)
            expr = sympy.expand(expr)
            if expr.is_Integer:
                return (int(expr), 0)
            s = sympy.Symbol('s')
            expr_s = expr.subs(sympy.sqrt(d), s)
            p = sympy.Poly(expr_s, s)
            coeffs = p.all_coeffs()
            for c in coeffs:
                if not c.is_Integer:
                    raise ValueError("Coefficients must be integers")
            if len(coeffs) == 1:
                return (int(coeffs[0]), 0)
            elif len(coeffs) == 2:
                return (int(coeffs[1]), int(coeffs[0]))
            else:
                raise ValueError("Not in Z[sqrt(d)]")
                
        return d, to_tuple(a_expr, d), to_tuple(b_expr, d), to_tuple(r_expr, d)
        
    raise ValueError("Could not parse witness")

def conditions(witness) -> list[bool]:
    try:
        parsed = parse_witness(witness)
        d = parsed[0]
        a = parsed[1]
        b = parsed[2]
        r_provided = parsed[3]
        
        if d >= 0:
            return [False, False]
        h1 = not is_zero(a) and not is_zero(b)
    except Exception:
        return [False, False]
        
    try:
        if not h1:
            return [h1, False]
            
        gcds = get_gcds(a, b, d)
        
        if not gcds:
            neg_q = True
        else:
            g = next(iter(gcds))
            neg_q = False
            if r_provided is not None:
                rb = mul(r_provided, b, d)
                ag = exact_div(a, g, d)
                if divides(a, rb, d) and not divides(ag, r_provided, d):
                    neg_q = True
            
            if not neg_q:
                r = find_r(a, b, g, d)
                if r is not None:
                    neg_q = True
                
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: The ideal quotient (a) : (b) is not equal to the principal ideal (a / gcd(a, b))"
]

N_HYP = 1
NEG_Q_INDEX = 1