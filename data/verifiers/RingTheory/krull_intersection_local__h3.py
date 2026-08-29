import math
import sympy
from sympy import symbols, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: witness is a tuple (modulus, m) representing Z/modulus and ideal (m)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            modulus, m = witness
            if isinstance(modulus, (int, sympy.Integer)) and isinstance(m, (int, sympy.Integer)):
                if not isinstance(modulus, bool) and not isinstance(m, bool):
                    modulus = int(modulus)
                    m = int(m)
                    if modulus >= 2:
                        h1 = True
                        h2 = True
                        stable_gcd = math.gcd(pow(m, modulus, modulus), modulus)
                        neg_q = (stable_gcd % modulus != 0)
                    return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Case 2: witness is an integer modulus representing Z/modulus
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            modulus = int(witness)
            if modulus >= 2:
                h1 = True
                h2 = True
                # Check if there is any maximal ideal m (prime factor of modulus)
                # such that the intersection of m^k is not the zero ideal.
                for i in range(2, modulus):
                    if modulus % i == 0:
                        is_prime = True
                        for j in range(2, int(math.isqrt(i)) + 1):
                            if i % j == 0:
                                is_prime = False
                                break
                        if is_prime:
                            stable_gcd = math.gcd(pow(i, modulus, modulus), modulus)
                            if stable_gcd % modulus != 0:
                                neg_q = True
                                break
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS: list[str] = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "¬Q: The intersection of m^n for all positive integers n is not the zero ideal"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2