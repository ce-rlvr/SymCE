import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, primitive_root
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (q, a, b) where:
      - q is the size of the finite field (a prime power).
      - a is an integer representing the multiplicative character chi (chi(g^k) = exp(2*pi*i*a*k/(q-1))).
      - b is an integer representing the additive character psi (psi(x) = exp(2*pi*i*b*x/p)).
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q', witness.get('p', 0))
            a = witness.get('a', witness.get('chi', 0))
            b = witness.get('b', witness.get('psi', 0))
        elif hasattr(witness, '__iter__') and not isinstance(witness, str):
            witness = list(witness)
            q, a, b = witness[0], witness[1], witness[2]
        else:
            return [False, False, False]
            
        q = int(q)
        a = int(a)
        b = int(b)
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field (q is a prime power)
    try:
        factors = factorint(q)
        h1 = (len(factors) == 1) and (q > 1)
        p = list(factors.keys())[0]
        r = factors[p]
    except Exception:
        h1 = False
        p = 0
        r = 0

    # H2: chi is a non-trivial multiplicative character of F_q
    try:
        h2 = (a % (q - 1)) != 0
    except Exception:
        h2 = False

    # neg_Q: The absolute value of the Gauss sum G(chi, psi) is NOT equal to sqrt(q)
    try:
        if not h1:
            neg_q = False
        elif r == 1:
            g = primitive_root(q)
            dlog = {}
            curr = 1
            for k in range(q - 1):
                dlog[curr] = k
                curr = (curr * g) % q
            
            term_sum = 0
            for x in range(1, q):
                k = dlog[x]
                term_sum += sp.exp(2 * sp.pi * sp.I * a * k / (q - 1)) * sp.exp(2 * sp.pi * sp.I * b * x / q)
            
            val = complex(term_sum.evalf(50))
            mag_sq = val.real**2 + val.imag**2
            # Check if magnitude squared is not equal to q
            neg_q = abs(mag_sq - q) > 1e-5
        else:
            # For prime powers q = p^r (r > 1), if b is a multiple of p, 
            # the additive character is trivial, making the Gauss sum exactly 0.
            if b % p == 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: chi is a non-trivial multiplicative character of F_q",
    "¬Q: The absolute value of the Gauss sum G(chi, psi) is not equal to sqrt(q)"
]

N_HYP = 2
NEG_Q_INDEX = 2