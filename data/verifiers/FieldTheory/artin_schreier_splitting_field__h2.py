import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the prime characteristic `p` and the element `a`.
    It can be a tuple (p, a), a tuple (F, p, a), or a dict {'p': p, 'a': a}.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                p, a = witness
            elif len(witness) == 3:
                _, p, a = witness
            else:
                p, a = None, None
        else:
            p, a = None, None
            
        if isinstance(a, (int, sympy.Integer)):
            a = int(a)
            a_is_int = True
        else:
            a_is_int = False
            
        h1 = bool(sympy.isprime(p) and a_is_int)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Prevent excessively large primes from hanging the verifier
            if p > 1000:
                neg_q = False
            else:
                x = sympy.Symbol('x')
                # Construct the polynomial x^p - x - a over GF(p)
                poly = sympy.Poly(x**p - x - a, domain=sympy.GF(p))
                factors = poly.factor_list()
                
                # The degree of the splitting field over GF(p) is the LCM of the degrees of its irreducible factors
                degrees = [f.degree() for f, m in factors[1]]
                deg_split = 1
                for d in degrees:
                    deg_split = (deg_split * d) // math.gcd(deg_split, d)
                
                # The conclusion claims the splitting field has degree p.
                # The negated conclusion is that the degree is NOT p.
                neg_q = bool(deg_split != p)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p",
    "¬Q: The splitting field of x^p - x - a over F does not have degree p"
]

N_HYP = 1
NEG_Q_INDEX = 1