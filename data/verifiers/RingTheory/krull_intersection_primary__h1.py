import math
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Symbol, Rational, Integer

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

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        n, d = None, None
        # The witness is expected to represent the ring Z/nZ and the ideal (d).
        # It can be provided as a tuple (n, d), a dict, or an object with n and d attributes.
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                n, d = int(witness[0]), int(witness[1])
            except (ValueError, TypeError):
                pass
        elif isinstance(witness, dict) and 'n' in witness and 'd' in witness:
            try:
                n, d = int(witness['n']), int(witness['d'])
            except (ValueError, TypeError):
                pass
        elif hasattr(witness, 'n') and hasattr(witness, 'd'):
            try:
                n, d = int(witness.n), int(witness.d)
            except (ValueError, TypeError):
                pass
                
        if n is not None and d is not None:
            n = abs(n)
            if n == 0:
                # In Z, the only primary ideals are (0) and (p^k).
                # The intersection of powers of any proper primary ideal in Z is always (0).
                d = abs(d)
                is_proper = (d != 1)
                is_primary = (d == 0 or len(factorint(d)) == 1)
                h1 = is_proper and is_primary
                neg_q = False
                return [h1, neg_q]
            elif n > 1:
                d = abs(d) % n
                g = math.gcd(d, n)
                
                # H1: Q is a proper primary ideal of R
                # In Z/nZ, (d) is proper iff gcd(d, n) > 1
                is_proper = (g > 1)
                
                # In Z/nZ, (d) is primary iff its preimage in Z is primary, 
                # which means gcd(d, n) must be a prime power.
                factors_g = factorint(g)
                is_primary = (len(factors_g) == 1)
                h1 = is_proper and is_primary
                
                # neg_Q: The intersection of all positive powers of Q is NOT the zero ideal.
                # The sequence of ideals (d^m) stabilizes to (0) iff every prime factor of n divides d.
                # Equivalently, iff the prime factors of n are a subset of the prime factors of g.
                factors_n = factorint(n)
                neg_q = not set(factors_n.keys()).issubset(set(factors_g.keys()))
                
                return [h1, neg_q]
    except Exception:
        pass

    # Fallback for custom objects with explicit methods
    try:
        if hasattr(witness, 'is_proper_primary') and hasattr(witness, 'intersection_is_zero'):
            h1 = bool(witness.is_proper_primary())
            neg_q = not bool(witness.intersection_is_zero())
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: Q is a proper primary ideal of R",
    "¬Q: The intersection of all positive powers of Q is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1