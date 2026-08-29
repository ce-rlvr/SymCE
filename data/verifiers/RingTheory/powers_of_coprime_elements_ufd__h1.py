import math
import sympy
from sympy import sqrt, expand, simplify
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

class Z_sqrt_d:
    """Representation of an element x + y*sqrt(d) in Z[sqrt(d)]."""
    def __init__(self, x, y, d):
        self.x = int(x)
        self.y = int(y)
        self.d = int(d)
    
    def __mul__(self, other):
        return Z_sqrt_d(
            self.x * other.x + self.d * self.y * other.y,
            self.x * other.y + self.y * other.x,
            self.d
        )
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.d == other.d
    
    def norm(self):
        return self.x**2 - self.d * self.y**2
        
    def __pow__(self, n):
        res = Z_sqrt_d(1, 0, self.d)
        base = self
        while n > 0:
            if n % 2 == 1:
                res = res * base
            base = base * base
            n //= 2
        return res

def parse_element(expr, d):
    if isinstance(expr, (tuple, list)):
        return Z_sqrt_d(int(expr[0]), int(expr[1]), d)
    
    expr = sympy.expand(expr)
    sq_d = sympy.sqrt(d)
    
    y = expr.coeff(sq_d)
    x = sympy.simplify(expr - y * sq_d)
    
    return Z_sqrt_d(int(x), int(y), d)

def divides(q, a):
    nq = q.norm()
    if nq == 0: return False
    conj_q = Z_sqrt_d(q.x, -q.y, q.d)
    prod = a * conj_q
    return prod.x % nq == 0 and prod.y % nq == 0

def is_relatively_prime(a, b):
    if a.d >= 0:
        return math.gcd(abs(a.norm()), abs(b.norm())) == 1
    
    d = a.d
    na = abs(a.norm())
    nb = abs(b.norm())
    
    limit = min(na, nb)
    abs_d = -d
    for nq in range(2, limit + 1):
        if na % nq == 0 and nb % nq == 0:
            max_y = int(math.isqrt(nq // abs_d))
            for y in range(-max_y - 1, max_y + 2):
                rem = nq - abs_d * y**2
                if rem < 0:
                    continue
                x = math.isqrt(rem)
                if x**2 == rem:
                    q1 = Z_sqrt_d(x, y, d)
                    q2 = Z_sqrt_d(-x, y, d)
                    for q in [q1, q2]:
                        if divides(q, a) and divides(q, b):
                            return False
    return True

def get_units(d):
    units = [Z_sqrt_d(1, 0, d), Z_sqrt_d(-1, 0, d)]
    if d == -1:
        units.extend([Z_sqrt_d(0, 1, d), Z_sqrt_d(0, -1, d)])
    return units

def is_nth_power(w, n):
    nw = abs(w.norm())
    if nw == 0:
        return True
    
    k = int(round(nw ** (1.0 / n)))
    while (k + 1) ** n <= nw:
        k += 1
    while k ** n > nw and k > 0:
        k -= 1
        
    if k ** n != nw:
        return False
    
    d = w.d
    abs_d = -d
    max_y = int(math.isqrt(k // abs_d))
    for y in range(-max_y - 1, max_y + 2):
        rem = k - abs_d * y**2
        if rem < 0:
            continue
        x = math.isqrt(rem)
        if x**2 == rem:
            cand1 = Z_sqrt_d(x, y, d)
            cand2 = Z_sqrt_d(-x, y, d)
            for cand in [cand1, cand2]:
                if cand**n == w:
                    return True
    return False

def has_power_representation(elem, n):
    d = elem.d
    if d >= 0:
        # We only rigorously support checking non-existence of powers in imaginary quadratic fields
        return True
    units = get_units(d)
    for u in units:
        u_inv = Z_sqrt_d(u.x, -u.y, d)
        w = elem * u_inv
        if is_nth_power(w, n):
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a_raw = witness['a']
            b_raw = witness['b']
            c_raw = witness['c']
            n = witness['n']
            d = witness.get('d', None)
        else:
            if len(witness) == 5:
                a_raw, b_raw, c_raw, n, d = witness
            elif len(witness) == 4:
                a_raw, b_raw, c_raw, n = witness
                d = None
            else:
                return [False] * 5
                
        if d is None:
            for raw in [a_raw, b_raw, c_raw]:
                sym = sympy.expand(raw)
                for arg in sym.atoms(sympy.Pow):
                    if arg.exp == sympy.S.Half:
                        base = arg.base
                        if base.is_Integer:
                            d = int(base)
                            if sym.has(sympy.I):
                                d = -d
                            break
                if d is not None:
                    break
            if d is None:
                for raw in [a_raw, b_raw, c_raw]:
                    if sympy.expand(raw).has(sympy.I):
                        d = -1
                        break
            if d is None:
                d = -1
                
        d = int(d)
        n = int(n)
        
        a = parse_element(a_raw, d)
        b = parse_element(b_raw, d)
        c = parse_element(c_raw, d)
        
        h1 = (a.x != 0 or a.y != 0) and (b.x != 0 or b.y != 0) and (c.x != 0 or c.y != 0)
        h2 = is_relatively_prime(a, b)
        h3 = n >= 2
        h4 = (a * b) == (c ** n)
        
        a_has_rep = has_power_representation(a, n)
        b_has_rep = has_power_representation(b, n)
        
        neg_q = not (a_has_rep and b_has_rep)
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero elements of R",
    "H_2: a and b are relatively prime",
    "H_3: n >= 2 is an integer",
    "H_4: ab = c^n",
    "¬Q: a is not of the form u x^n or b is not of the form v y^n"
]

N_HYP = 4
NEG_Q_INDEX = 4