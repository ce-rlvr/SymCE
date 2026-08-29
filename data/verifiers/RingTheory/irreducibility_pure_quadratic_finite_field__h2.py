import sympy
from sympy import Symbol, Poly, GF, Rational
from sympy.ntheory import isprime, legendre_symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: The equivalence (x^2 - a is irreducible over F_p iff (a/p) = -1) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        p, a = witness
    except Exception:
        return [False, False]
        
    # H_1: p is an odd prime number
    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    # ¬Q: The equivalence fails
    # The equivalence is: x^2 - a is irreducible over F_p iff (a/p) = -1
    try:
        x = Symbol('x')
        # Handle the case where 'a' is a rational number (a common counterexample when the "a is an integer" hypothesis is dropped)
        if hasattr(a, 'is_Rational') and a.is_Rational and not a.is_Integer:
            a_mod = (a.p * pow(a.q, -1, p)) % p
            poly = Poly(x**2 - a_mod, domain=GF(p))
        else:
            poly = Poly(x**2 - a, domain=GF(p))
        is_irred = bool(poly.is_irreducible)
    except Exception:
        is_irred = False

    try:
        leg = legendre_symbol(a, p)
        leg_is_minus_one = bool(leg == -1)
    except Exception:
        leg_is_minus_one = False

    try:
        q = (is_irred == leg_is_minus_one)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]