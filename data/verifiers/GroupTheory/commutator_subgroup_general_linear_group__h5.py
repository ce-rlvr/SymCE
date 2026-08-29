import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix, eye, zeros
from sympy.abc import x
from sympy.polys.domains import ZZ, QQ
import sympy.ntheory
import itertools
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

CONDITION_LABELS = [
    "H_1: Let F be a field",
    "H_2: Let n be a positive integer",
    "H_3: Assume that either n >= 3, or both n = 2 and |F| > 3",
    "H_4: Let GL_n(F) be the general linear group of degree n over F",
    "¬Q: The commutator subgroup of GL_n(F) is not SL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def is_prime_power(q):
    if not isinstance(q, int) or q < 2:
        return False
    for p in sympy.primerange(2, int(math.sqrt(q)) + 2):
        if q % p == 0:
            k = q
            while k % p == 0:
                k //= p
            return k == 1
    return sympy.isprime(q)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (n, q) representing the degree n and the size of the finite field F_q.
    """
    try:
        n, q = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: Let F be a field
    try:
        h1_ok = is_prime_power(q)
    except Exception:
        h1_ok = False

    # H_2: Let n be a positive integer
    try:
        h2_ok = isinstance(n, int) and n > 0
    except Exception:
        h2_ok = False

    # H_3: Assume that either n >= 3, or both n = 2 and |F| > 3
    try:
        h3_ok = (n >= 3) or (n == 2 and q > 3)
    except Exception:
        h3_ok = False

    # H_4: Let GL_n(F) be the general linear group of degree n over F
    # This is a definitional hypothesis, trivially true if the previous ones hold.
    h4_ok = True

    # neg_Q: The commutator subgroup of GL_n(F) is NOT SL_n(F)
    # Mathematically, [GL_n(F), GL_n(F)] = SL_n(F) for all fields F and n >= 1,
    # EXCEPT when n = 2 and |F| = 2, where [GL_2(2), GL_2(2)] = A_3 != SL_2(2).
    try:
        neg_q_ok = (n == 2 and q == 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]