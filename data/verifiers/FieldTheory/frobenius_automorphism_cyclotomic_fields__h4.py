import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_zero(expr):
    try:
        if expr == 0:
            return True
    except Exception:
        pass
    try:
        if sympy.simplify(expr) == 0:
            return True
    except Exception:
        pass
    try:
        if abs(complex(expr)) < 1e-9:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    witness is expected to be a tuple: (n, p, zeta_n, sigma_p)
    where sigma_p is a callable representing the automorphism/function.
    """
    try:
        n, p, zeta_n, sigma_p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: p is a prime number that does not divide n
    try:
        h2 = sympy.ntheory.isprime(p) and (n % p != 0)
    except Exception:
        h2 = False

    # H_3: zeta_n is a primitive n-th root of unity in C
    try:
        if not h1:
            h3 = False
        else:
            if not is_zero(zeta_n**n - 1):
                h3 = False
            else:
                h3 = True
                for d in sympy.ntheory.divisors(n)[:-1]:
                    if is_zero(zeta_n**d - 1):
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: sigma_p(zeta_n) != zeta_n**p
    try:
        lhs = sigma_p(zeta_n)
        rhs = zeta_n**p
        neg_q = not is_zero(lhs - rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is a prime number that does not divide n",
    "H_3: zeta_n is a primitive n-th root of unity in C",
    "¬Q: sigma_p(zeta_n) != zeta_n**p"
]

N_HYP = 3
NEG_Q_INDEX = 3