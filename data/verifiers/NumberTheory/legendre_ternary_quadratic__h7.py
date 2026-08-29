import math
import itertools
import functools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, legendre_symbol
from sympy.abc import x, y, z

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

def is_quad_residue_mod(n, m):
    m = abs(m)
    if m == 1:
        return True
    if m == 0:
        return False
    factors = factorint(m)
    for p, exp in factors.items():
        if p == 2:
            if exp >= 2:
                if n % 4 not in (0, 1):
                    return False
            if exp >= 3:
                if n % 8 not in (0, 1, 4):
                    return False
            continue
        if legendre_symbol(n, p) == -1:
            return False
    return True

def has_nontrivial_solution(a, b, c):
    if a == 0 or b == 0 or c == 0:
        return False
    if (a > 0 and b > 0 and c > 0) or (a < 0 and b < 0 and c < 0):
        return False
        
    # 1. Try Holzer bounds first (very fast and guaranteed for valid witnesses)
    try:
        X = math.isqrt(abs(b * c)) + 1
        Y = math.isqrt(abs(a * c)) + 1
        X = min(X, 1000)
        Y = min(Y, 1000)
        for i in range(X + 1):
            for j in range(Y + 1):
                if i == 0 and j == 0:
                    continue
                val = -(a * i**2 + b * j**2)
                if val % c == 0:
                    z2 = val // c
                    if z2 >= 0:
                        s = math.isqrt(z2)
                        if s * s == z2:
                            return True
    except Exception:
        pass

    # 2. Try sympy diophantine solver
    try:
        sols = sympy.diophantine(a*x**2 + b*y**2 + c*z**2)
        for sol in sols:
            if any(str(comp) != '0' for comp in sol):
                return True
        return False
    except Exception:
        pass
        
    # 3. Fallback to Legendre's condition (mathematically equivalent for valid witnesses)
    try:
        return is_quad_residue_mod(-a*b, c) and is_quad_residue_mod(-b*c, a) and is_quad_residue_mod(-a*c, b)
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 7
        a, b, c = witness
    except Exception:
        return [False] * 7

    try:
        h1 = isinstance(a, int) and not isinstance(a, bool) and \
             isinstance(b, int) and not isinstance(b, bool) and \
             isinstance(c, int) and not isinstance(c, bool) and \
             a != 0 and b != 0 and c != 0
    except Exception:
        h1 = False

    try:
        def sq_free(n):
            if n == 0: return False
            factors = factorint(abs(n))
            return all(v == 1 for v in factors.values())
        h2 = sq_free(a) and sq_free(b) and sq_free(c)
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(a, b) == 1 and math.gcd(b, c) == 1 and math.gcd(a, c) == 1
    except Exception:
        h3 = False

    try:
        h4 = not ((a > 0 and b > 0 and c > 0) or (a < 0 and b < 0 and c < 0))
    except Exception:
        h4 = False

    try:
        h5 = is_quad_residue_mod(-b * c, a)
    except Exception:
        h5 = False

    try:
        h6 = is_quad_residue_mod(-a * c, b)
    except Exception:
        h6 = False

    try:
        neg_q = not has_nontrivial_solution(a, b, c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero integers",
    "H_2: a, b, c are square-free",
    "H_3: gcd(a, b) = 1, gcd(b, c) = 1, and gcd(a, c) = 1",
    "H_4: a, b, c do not all have the same sign",
    "H_5: -bc is a quadratic residue modulo a",
    "H_6: -ac is a quadratic residue modulo b",
    "¬Q: There do not exist integers x, y, z, not all zero, such that ax^2 + by^2 + cz^2 = 0"
]

N_HYP = 6
NEG_Q_INDEX = 6