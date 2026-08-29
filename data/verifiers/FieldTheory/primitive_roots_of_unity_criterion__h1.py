import math
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def _lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def is_prime_power(q):
    if q <= 1:
        return False
    factors = factorint(q)
    return len(factors) == 1

def carmichael_lambda(q):
    """Computes the Carmichael lambda function of q, which is the exponent of the group (Z/qZ)*."""
    if q <= 0: return 0
    if q == 1: return 1
    factors = factorint(q)
    res = 1
    for p, e in factors.items():
        if p == 2:
            if e == 1: l = 1
            elif e == 2: l = 2
            else: l = 2**(e - 2)
        else:
            l = (p - 1) * (p**(e - 1))
        res = _lcm(res, l)
    return res

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, q).
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
        else:
            n, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # H_2: n is coprime to q
    try:
        h2 = isinstance(q, int) and q > 0 and math.gcd(n, q) == 1
    except Exception:
        h2 = False
        
    # ¬Q: The equivalence (F_q contains a primitive n-th root of unity iff n divides q-1) FAILS
    try:
        if not (isinstance(q, int) and q > 0 and isinstance(n, int) and n > 0):
            neg_q = False
        else:
            # Right hand side of the iff: n divides q-1
            rhs = ((q - 1) % n == 0)
            
            if is_prime_power(q):
                # If q is a prime power, F_q is a valid finite field.
                # Its multiplicative group is cyclic of order q-1, so it ALWAYS 
                # contains an element of order n iff n divides q-1.
                lhs = rhs
            else:
                # If q is not a prime power, F_q is technically undefined, but in this context 
                # it is evaluated as the ring Z/qZ. We check if Z/qZ has an element of order n.
                # A finite abelian group has an element of order n iff n divides its exponent.
                lhs = (carmichael_lambda(q) % n == 0)
                
            # The conclusion fails if the left-hand side and right-hand side of the iff do not match
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: n is coprime to q",
    "¬Q: The equivalence (F_q contains a primitive n-th root of unity iff n divides q-1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2