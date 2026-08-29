import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring_element(expr):
    if isinstance(expr, (int, sympy.Integer)):
        return True
    if hasattr(expr, 'is_integer') and expr.is_integer:
        return True
    try:
        if expr.is_Rational:
            return False
        poly = sympy.Poly(expr)
        return all(c.is_integer for c in poly.coeffs())
    except Exception:
        return False

def divides(x, y):
    if hasattr(x, 'divides'):
        return x.divides(y)
    if hasattr(y, 'is_divisible_by'):
        return y.is_divisible_by(x)
    if isinstance(x, sympy.MatrixBase) and isinstance(y, sympy.MatrixBase):
        try:
            z = x.inv() * y
            if all(e.is_integer for e in z):
                return True
        except Exception:
            pass
        try:
            z = y * x.inv()
            if all(e.is_integer for e in z):
                return True
        except Exception:
            pass
        return False
        
    try:
        if y % x == 0:
            return True
    except Exception:
        pass
        
    try:
        q = sympy.simplify(y / x)
        q_simp = sympy.radsimp(q)
        if is_ring_element(q_simp):
            return True
        q_expand = sympy.expand(q_simp)
        if is_ring_element(q_expand):
            return True
    except Exception:
        pass
    return False

def get_generators(exprs):
    gens = set()
    for expr in exprs:
        if isinstance(expr, sympy.Expr):
            sqrts = [s for s in expr.atoms(sympy.Pow) if s.exp == sympy.Rational(1, 2)]
            for s in sqrts:
                gens.add(s)
            if expr.has(sympy.I):
                gens.add(sympy.I)
    
    gens = list(gens)
    if len(gens) == 2 and sympy.I in gens:
        other = gens[0] if gens[1] == sympy.I else gens[1]
        if other.is_Pow and other.exp == sympy.Rational(1, 2):
            return [sympy.I * other]
    return gens

def are_coprime(a, b):
    if hasattr(a, 'coprime'):
        return a.coprime(b)
    if isinstance(a, int) and isinstance(b, int):
        return math.gcd(a, b) == 1
        
    try:
        gens = get_generators([a, b])
        if len(gens) == 0:
            return sympy.gcd(a, b) == 1
        if len(gens) == 1:
            g = gens[0]
            g2 = sympy.simplify(g**2)
            if g2.is_Rational:
                def norm(x):
                    return sympy.simplify(x * x.subs(g, -g))
                
                na = abs(sympy.Integer(norm(a)))
                nb = abs(sympy.Integer(norm(b)))
                gcd_norm = sympy.gcd(na, nb)
                
                if gcd_norm == 1:
                    return True
                    
                x, y = a, b
                for _ in range(20):
                    if y == 0:
                        break
                    nx = abs(sympy.Integer(norm(x)))
                    ny = abs(sympy.Integer(norm(y)))
                    if nx < ny:
                        x, y = y, x
                    
                    ratio = sympy.expand(sympy.radsimp(sympy.simplify(x / y)))
                    if ratio.is_Add:
                        terms = ratio.args
                    else:
                        terms = (ratio,)
                    
                    q = 0
                    for t in terms:
                        if t.is_Rational:
                            q += round(float(t))
                        elif t.is_Mul:
                            c = [arg for arg in t.args if arg != g]
                            if len(c) == 1 and c[0].is_Rational:
                                q += round(float(c[0])) * g
                        elif t == g:
                            q += g
                        elif t == -g:
                            q -= g
                    
                    rem = sympy.simplify(x - q * y)
                    if rem == x:
                        break
                    x, y = y, rem
                
                if y == 0:
                    nx = abs(sympy.Integer(norm(x)))
                    if nx > 1:
                        return False
                else:
                    nx = abs(sympy.Integer(norm(x)))
                    if nx > 1 and divides(x, a) and divides(x, b):
                        return False
                    ny = abs(sympy.Integer(norm(y)))
                    if ny > 1 and divides(y, a) and divides(y, b):
                        return False
                
                if g2 < 0:
                    abs_g2 = abs(g2)
                    max_v = int(sympy.sqrt(gcd_norm / abs_g2)) + 1
                    max_u = int(sympy.sqrt(gcd_norm)) + 1
                    
                    for v in range(-max_v, max_v + 1):
                        for u in range(-max_u, max_u + 1):
                            if u == 0 and v == 0:
                                continue
                            d = u + v * g
                            nd = u**2 + abs_g2 * v**2
                            if nd > 1 and gcd_norm % nd == 0:
                                conj_d = u - v * g
                                q_a = sympy.expand(a * conj_d)
                                q_b = sympy.expand(b * conj_d)
                                try:
                                    poly_a = sympy.Poly(q_a, g)
                                    poly_b = sympy.Poly(q_b, g)
                                    if all(c % nd == 0 for c in poly_a.coeffs()) and all(c % nd == 0 for c in poly_b.coeffs()):
                                        return False
                                except Exception:
                                    if divides(d, a) and divides(d, b):
                                        return False
                    return True
                else:
                    poly_a = sympy.Poly(a, g)
                    poly_b = sympy.Poly(b, g)
                    cont_a = sympy.gcd_list(poly_a.coeffs())
                    cont_b = sympy.gcd_list(poly_b.coeffs())
                    if sympy.gcd(cont_a, cont_b) > 1:
                        return False
                    return True
    except Exception:
        pass
        
    try:
        if sympy.gcd(a, b) == 1:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = (a != 0) and (b != 0) and (c != 0)
        if hasattr(a, 'is_zero_matrix') and a.is_zero_matrix: h1 = False
        if hasattr(b, 'is_zero_matrix') and b.is_zero_matrix: h1 = False
        if hasattr(c, 'is_zero_matrix') and c.is_zero_matrix: h1 = False
    except Exception:
        h1 = False
        
    try:
        bc = b * c
        h2 = divides(a, bc)
    except Exception:
        h2 = False
        
    try:
        h3 = are_coprime(a, b)
    except Exception:
        h3 = False
        
    try:
        neg_q = not divides(a, c)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements of R",
    "H_2: a divides the product bc",
    "H_3: a and b are coprime",
    "¬Q: a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3