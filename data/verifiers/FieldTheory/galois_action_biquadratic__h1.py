import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Poly, cancel, fraction
from sympy.abc import x, y, z, t
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

def is_square_poly(P_expr, p):
    P_expr = sympy.sympify(P_expr)
    syms = P_expr.free_symbols
    if not syms:
        gen = x
    else:
        gen = list(syms)[0]
        
    if p == 0:
        P = Poly(P_expr, gen, domain='QQ')
        if P.is_zero:
            return True
        c, factors = P.factor_list()
        c_num, c_den = c.as_numer_denom()
        if c < 0:
            return False
        if math.isqrt(int(c_num))**2 != int(c_num):
            return False
        if math.isqrt(int(c_den))**2 != int(c_den):
            return False
        return all(mult % 2 == 0 for f, mult in factors)
    else:
        from sympy import GF
        P = Poly(P_expr, gen, domain=GF(p))
        if P.is_zero:
            return True
        if p == 2:
            return all(deg[0] % 2 == 0 for deg in P.monoms())
        else:
            c, factors = P.factor_list()
            c = int(c) % p
            if c != 0 and pow(c, (p-1)//2, p) != 1:
                return False
            return all(mult % 2 == 0 for f, mult in factors)

def is_square_rat(f_expr, p):
    f_expr = cancel(f_expr)
    num, den = fraction(f_expr)
    return is_square_poly(num * den, p)

def conditions(witness):
    """
    witness is expected to be a tuple (p, a, b) where:
      - p is the characteristic of the field K (a prime integer, or 0 for Q)
      - a and b are rational functions in x over K
    """
    try:
        p, a, b = witness
        
        # Check H_1: a, b, and a*b are not squares in K
        a_is_sq = is_square_rat(a, p)
        b_is_sq = is_square_rat(b, p)
        ab_is_sq = is_square_rat(a * b, p)
        
        h1 = not a_is_sq and not b_is_sq and not ab_is_sq
        
        # Check neg_Q: The Galois group is NOT isomorphic to the Klein four-group.
        # In characteristic != 2, if H_1 holds, the extension is a separable biquadratic 
        # extension, so the Galois group is always V4.
        # In characteristic 2, the extension is purely inseparable, so the automorphism 
        # group (Galois group) is trivial (size 1), which is not V4.
        # Thus, the conclusion fails iff p == 2.
        neg_q = (p == 2)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: a, b, and ab are not squares in K",
    "¬Q: The Galois group is not isomorphic to the Klein four-group (e.g. char K = 2)"
]

N_HYP = 1
NEG_Q_INDEX = 1