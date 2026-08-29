import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, isprime
import math

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

def is_sq(n):
    if n < 0:
        return False
    if n == 0:
        return True
    s = math.isqrt(n)
    return s * s == n

def conditions(witness) -> list[bool]:
    # H_1: p is an odd prime number
    try:
        if isinstance(witness, (int, sympy.Integer)):
            p = int(witness)
            h1 = (p % 2 != 0) and isprime(p)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The field ℚ(ζ_p) does NOT contain exactly one quadratic subfield over ℚ,
    # OR it is not equal to ℚ(√((-1)^{(p-1)/2} p)).
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            neg_q = True
        else:
            p = int(witness)
            if p <= 0:
                neg_q = True
            else:
                # Calculate the number of Z/2Z quotients in the Galois group (Z/pZ)*
                factors = factorint(p)
                c = 0
                for q, k in factors.items():
                    if q == 2:
                        if k == 2:
                            c += 1
                        elif k >= 3:
                            c += 2
                    else:
                        c += 1
                
                # The number of quadratic subfields is 2^c - 1.
                # It contains exactly one quadratic subfield iff c == 1.
                if c != 1:
                    neg_q = True
                else:
                    # Determine the actual unique quadratic subfield Q(sqrt(actual_d))
                    if 2 in factors and factors[2] == 2 and len(factors) == 1:
                        actual_d = -1
                    else:
                        q_odd = [q for q in factors if q != 2][0]
                        actual_d = q_odd if q_odd % 4 == 1 else -q_odd
                    
                    # Check if it matches the formula Q(sqrt((-1)^{(p-1)/2} p))
                    formula_d = ((-1)**((p - 1) // 2)) * p
                    
                    # Two quadratic fields Q(sqrt(d1)) and Q(sqrt(d2)) are equal iff d1*d2 is a square
                    prod = actual_d * formula_d
                    if prod > 0 and is_sq(prod):
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: ℚ(ζ_p) does not contain exactly one quadratic subfield, or it is not equal to ℚ(√((-1)^{(p-1)/2} p))"
]

N_HYP = 1
NEG_Q_INDEX = 1