import sympy as sp
from sympy import Poly, eye, zeros
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        p, m = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a field of prime characteristic p
    try:
        h1 = bool(sp.isprime(p))
    except Exception:
        h1 = False
        
    # H2: m(x) is the minimal polynomial of alpha over F
    # This implies m(x) must be a monic polynomial of degree >= 1 over GF(p)
    try:
        poly_m = Poly(m, x, domain=sp.GF(p))
        h2 = bool(poly_m.degree() >= 1 and poly_m.LC() == 1)
    except Exception:
        h2 = False
        
    # ¬Q: Negated conclusion
    # The conclusion states: there exists e >= 0 and a separable irreducible g(x) such that m(x) = g(x^{p^e})
    # We check if this holds. If it does NOT hold, the negated conclusion is True.
    try:
        poly_m = Poly(m, x, domain=sp.GF(p))
        deg = poly_m.degree()
        
        conclusion_holds = False
        if deg >= 1:
            e = 0
            while p**e <= deg:
                pe = p**e
                monoms = poly_m.monoms()
                # Check if m(x) can be written as a polynomial in x^{p^e}
                if all(deg_x[0] % pe == 0 for deg_x in monoms):
                    # Construct g(y) where m(x) = g(x^{p^e})
                    g_dict = {(deg_x[0] // pe,): coeff for deg_x, coeff in zip(monoms, poly_m.coeffs())}
                    g_poly = Poly.from_dict(g_dict, x, domain=sp.GF(p))
                    
                    # Check if g is irreducible over GF(p)
                    is_irred = bool(g_poly.is_irreducible)
                    
                    # Check if g is separable over GF(p) (i.e., gcd(g, g') == 1)
                    g_deriv = g_poly.diff()
                    if g_deriv.is_zero:
                        is_sep = False
                    else:
                        gcd_poly = g_poly.gcd(g_deriv)
                        is_sep = bool(gcd_poly.degree() == 0)
                        
                    if is_irred and is_sep:
                        conclusion_holds = True
                        break
                e += 1
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p",
    "H_2: m(x) is the minimal polynomial of alpha over F (m(x) is monic)",
    "¬Q: For all e >= 0 and separable irreducible g(x), m(x) != g(x^{p^e})"
]

N_HYP = 2
NEG_Q_INDEX = 2