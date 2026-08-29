import sympy
from sympy import symbols, Poly, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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
O2 = zeros(2,2)
O3 = zeros(3,3)

x = symbols('x')

def is_in_F(a, F):
    """Check if element a belongs to the field F."""
    try:
        if hasattr(F, 'from_sympy'):
            F.from_sympy(sympy.sympify(a))
            return True
        return sympy.sympify(a) in F
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false Capelli's Irreducibility Theorem conjecture.
    The dropped hypothesis is that a must be an element of F.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            n = witness.get('n')
            a = witness.get('a')
        else:
            F, n, a = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: n >= 2 is an integer
    try:
        h2 = isinstance(n, (int, Integer)) and n >= 2
    except Exception:
        h2 = False

    # H_3: For every prime number p dividing n, there is no element b in F such that b^p = a
    try:
        h3 = True
        if h2:
            primes = sympy.ntheory.factorint(n).keys()
            for p in primes:
                if not is_in_F(a, F):
                    # If a is not in F, no element b in F can satisfy b^p = a
                    continue
                rts = sympy.roots(x**p - a, x, domain=F)
                if len(rts) > 0:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # H_4: If 4 divides n, there is no element c in F such that a = -4c^4
    try:
        h4 = True
        if h2 and n % 4 == 0:
            if not is_in_F(a, F):
                pass # If a is not in F, no element c in F can satisfy -4c^4 = a
            else:
                rts = sympy.roots(4*x**4 + a, x, domain=F)
                if len(rts) > 0:
                    h4 = False
    except Exception:
        h4 = False

    # ¬Q: The polynomial x^n - a is reducible over F (or not a valid polynomial over F)
    try:
        if not is_in_F(a, F):
            # If a is not in F, x^n - a is not in F[x], so it cannot be irreducible over F.
            neg_q = True
        else:
            poly = Poly(x**n - a, x, domain=F)
            # It fails the conclusion if it is NOT irreducible
            neg_q = (poly.is_irreducible is False)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n >= 2 is an integer",
    "H_3: For every prime number p dividing n, there is no element b in F such that b^p = a",
    "H_4: If 4 divides n, there is no element c in F such that a = -4c^4",
    "¬Q: The polynomial x^n - a is reducible over F (or not a valid polynomial over F)"
]

N_HYP = 4
NEG_Q_INDEX = 4