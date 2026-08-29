import sympy as sp
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

class ZnPolynomial:
    """
    Represents a degree 1 polynomial ax + b in the ring Z_n[x].
    """
    def __init__(self, n, a, b):
        self.n = int(n)
        self.a = int(a) % self.n
        self.b = int(b) % self.n

    def __repr__(self):
        return f"ZnPolynomial(n={self.n}, a={self.a}, b={self.b})"

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, ZnPolynomial):
            n, a, b = witness.n, witness.a, witness.b
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n, a, b = witness
            n = int(n)
            a = int(a) % n
            b = int(b) % n
        else:
            # Try to interpret as sympy expression in x over ZZ
            x = sp.Symbol('x')
            expr = sp.sympify(witness)
            p = sp.Poly(expr, x, domain='ZZ')
            if p.degree() != 1:
                return [False, False]
            h1 = True
            coeffs = p.all_coeffs()
            prim = (math.gcd(abs(int(coeffs[0])), abs(int(coeffs[1]))) == 1)
            irr = p.is_irreducible
            neg_q = (irr != prim)
            return [h1, neg_q]
            
        if n < 2:
            return [False, False]
            
        h1 = (a != 0)
        
        prim = (math.gcd(a, math.gcd(b, n)) == 1)
        
        def is_poly_unit(p_tuple, mod_n):
            c2, c1, c0 = p_tuple
            if math.gcd(c0, mod_n) != 1: return False
            def is_nilp(x_val):
                curr = x_val % mod_n
                for _ in range(mod_n):
                    if curr == 0: return True
                    curr = (curr * x_val) % mod_n
                return False
            return is_nilp(c1) and is_nilp(c2)
            
        is_u = False
        if math.gcd(b, n) == 1:
            curr = a % n
            nilpotent = False
            for _ in range(n):
                if curr == 0:
                    nilpotent = True
                    break
                curr = (curr * a) % n
            is_u = nilpotent
            
        if is_u:
            irreducible = False
        else:
            if n <= 30:
                polys = [(c2, c1, c0) for c2 in range(n) for c1 in range(n) for c0 in range(n)]
                non_units = [p for p in polys if not is_poly_unit(p, n)]
                
                found_factorization = False
                for p1 in non_units:
                    if found_factorization: break
                    c2, c1, c0 = p1
                    for d0 in range(n):
                        if (c0 * d0) % n == b:
                            target_d1 = (a - c1*d0) % n
                            for d1 in range(n):
                                if (c0 * d1) % n == target_d1:
                                    target_d2 = (-c2*d0 - c1*d1) % n
                                    for d2 in range(n):
                                        if (c0 * d2) % n == target_d2:
                                            if (c2 * d1 + c1 * d2) % n == 0 and (c2 * d2) % n == 0:
                                                if not is_poly_unit((d2, d1, d0), n):
                                                    found_factorization = True
                                                    break
                                    if found_factorization: break
                            if found_factorization: break
                irreducible = not found_factorization
            else:
                irreducible = False
                
        neg_q = (irreducible != prim)
        return [h1, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial of degree 1",
    "¬Q: f(x) is irreducible iff f(x) is primitive is FALSE"
]
N_HYP = 1
NEG_Q_INDEX = 1