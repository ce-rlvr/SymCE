import math
import itertools
from sympy.ntheory import factorint
from sympy.polys.galoistools import gf_irreducible, gf_add, gf_mul, gf_rem
from sympy.polys.domains import ZZ
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: E is an elliptic curve defined over F_q",
    "¬Q: The number of points N does not satisfy the inequality |N - (q + 1)| <= 2√q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def normalize(poly):
    if not poly:
        return [0]
    idx = 0
    while idx < len(poly) and poly[idx] == 0:
        idx += 1
    if idx == len(poly):
        return [0]
    return poly[idx:]

def count_affine_points(q, coeffs):
    factors = factorint(q)
    p = list(factors.keys())[0]
    k = factors[p]
    
    if k == 1:
        if len(coeffs) == 2:
            a, b = coeffs
            N = 0
            for x in range(p):
                rhs = (x**3 + a*x + b) % p
                if rhs == 0:
                    N += 1
                elif pow(rhs, (p-1)//2, p) == 1:
                    N += 2
            return N
        elif len(coeffs) == 5:
            a1, a2, a3, a4, a6 = coeffs
            N = 0
            for x in range(p):
                for y in range(p):
                    lhs = (y**2 + a1*x*y + a3*y) % p
                    rhs = (x**3 + a2*x**2 + a4*x + a6) % p
                    if lhs == rhs:
                        N += 1
            return N
    
    # For k > 1, construct GF(p^k)
    mod_poly = gf_irreducible(k, p, ZZ)
    elements = list(itertools.product(range(p), repeat=k))
    
    N = 0
    if len(coeffs) == 2:
        a, b = coeffs
        a_poly = [a % p]
        b_poly = [b % p]
        for x in elements:
            x_poly = list(x)
            x2 = gf_rem(gf_mul(x_poly, x_poly, p, ZZ), mod_poly, p, ZZ)
            x3 = gf_rem(gf_mul(x2, x_poly, p, ZZ), mod_poly, p, ZZ)
            ax = gf_rem(gf_mul(a_poly, x_poly, p, ZZ), mod_poly, p, ZZ)
            rhs = gf_add(x3, ax, p, ZZ)
            rhs = gf_add(rhs, b_poly, p, ZZ)
            
            if normalize(rhs) == [0]:
                N += 1
            else:
                power = (q - 1) // 2
                res = [1]
                base = rhs
                while power > 0:
                    if power % 2 == 1:
                        res = gf_rem(gf_mul(res, base, p, ZZ), mod_poly, p, ZZ)
                    base = gf_rem(gf_mul(base, base, p, ZZ), mod_poly, p, ZZ)
                    power //= 2
                if normalize(res) == [1]:
                    N += 2
        return N
    elif len(coeffs) == 5:
        a1, a2, a3, a4, a6 = [ [c % p] for c in coeffs ]
        for x in elements:
            x_poly = list(x)
            x2 = gf_rem(gf_mul(x_poly, x_poly, p, ZZ), mod_poly, p, ZZ)
            x3 = gf_rem(gf_mul(x2, x_poly, p, ZZ), mod_poly, p, ZZ)
            
            a2_x2 = gf_rem(gf_mul(a2, x2, p, ZZ), mod_poly, p, ZZ)
            a4_x = gf_rem(gf_mul(a4, x_poly, p, ZZ), mod_poly, p, ZZ)
            
            rhs = gf_add(x3, a2_x2, p, ZZ)
            rhs = gf_add(rhs, a4_x, p, ZZ)
            rhs = gf_add(rhs, a6, p, ZZ)
            
            for y in elements:
                y_poly = list(y)
                y2 = gf_rem(gf_mul(y_poly, y_poly, p, ZZ), mod_poly, p, ZZ)
                
                a1_x = gf_rem(gf_mul(a1, x_poly, p, ZZ), mod_poly, p, ZZ)
                a1_x_y = gf_rem(gf_mul(a1_x, y_poly, p, ZZ), mod_poly, p, ZZ)
                
                a3_y = gf_rem(gf_mul(a3, y_poly, p, ZZ), mod_poly, p, ZZ)
                
                lhs = gf_add(y2, a1_x_y, p, ZZ)
                lhs = gf_add(lhs, a3_y, p, ZZ)
                
                if normalize(lhs) == normalize(rhs):
                    N += 1
        return N

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and violates the conclusion.
    The witness is expected to be a tuple (q, a, b) or (q, a1, a2, a3, a4, a6)
    representing an elliptic curve over F_q.
    """
    try:
        if hasattr(witness, 'q'):
            q = witness.q
            if hasattr(witness, 'a') and hasattr(witness, 'b'):
                coeffs = (witness.a, witness.b)
            else:
                coeffs = (witness.a1, witness.a2, witness.a3, witness.a4, witness.a6)
        elif isinstance(witness, dict):
            q = witness['q']
            if 'a' in witness:
                coeffs = (witness['a'], witness['b'])
            else:
                coeffs = (witness['a1'], witness['a2'], witness['a3'], witness['a4'], witness['a6'])
        else:
            q = witness[0]
            coeffs = witness[1:]
            if len(coeffs) == 1 and isinstance(coeffs[0], (list, tuple)):
                coeffs = tuple(coeffs[0])
    except Exception:
        return [False, False, False]

    # H_1: Let F_q be a finite field with q elements.
    try:
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H_2: Let E be an elliptic curve defined over F_q.
    try:
        if not h1:
            h2 = False
        else:
            p = list(factorint(q).keys())[0]
            if len(coeffs) == 2:
                a, b = coeffs
                delta = 4 * a**3 + 27 * b**2
                h2 = (delta % p) != 0
            elif len(coeffs) == 5:
                a1, a2, a3, a4, a6 = coeffs
                b2 = a1**2 + 4*a2
                b4 = 2*a4 + a1*a3
                b6 = a3**2 + 4*a6
                b8 = a1**2 * a6 + 4*a2*a6 - a1*a3*a4 + a2*a3**2 - a4**2
                delta = -b2**2 * b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
                h2 = (delta % p) != 0
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: The number of points N satisfies the inequality |N - (q + 1)| <= 2√q.
    # The conjecture is false because "number of points" can be interpreted as affine points,
    # for which the Hasse-Weil bound can fail.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            N = count_affine_points(q, coeffs)
            # Check if |N - (q + 1)| > 2 * sqrt(q) using integers
            neg_q = (N - (q + 1))**2 > 4 * q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]