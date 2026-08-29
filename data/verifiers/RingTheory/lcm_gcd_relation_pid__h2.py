import sympy
import math
import itertools
import functools
import z3
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def divides(u, v, R):
    """Check if u divides v in the ring R."""
    if u == 0 or getattr(u, 'is_zero', False) or u == getattr(R, 'zero', None):
        return v == 0 or getattr(v, 'is_zero', False) or v == getattr(R, 'zero', None)
    
    if hasattr(R, 'exquo'):
        try:
            R.exquo(v, u)
            return True
        except Exception:
            return False

    if hasattr(R, 'rem'):
        try:
            rem = R.rem(v, u)
            if rem == 0 or getattr(rem, 'is_zero', False) or rem == getattr(R, 'zero', None):
                return True
        except Exception:
            pass

    try:
        rem = v % u
        if rem == 0 or getattr(rem, 'is_zero', False):
            return True
        if isinstance(rem, sympy.Expr):
            if sympy.simplify(rem) == 0:
                return True
    except Exception:
        pass

    try:
        if v == u * (v // u):
            return True
    except Exception:
        pass

    return False

def is_associate(u, v, R):
    """Check if u and v are associate in the ring R."""
    return divides(u, v, R) and divides(v, u, R)

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to provide the ring R, elements a and b, 
    a greatest common divisor d, and a least common multiple m.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            a = witness.get('a')
            b = witness.get('b')
            d = witness.get('d')
            m = witness.get('m')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 5:
                R, a, b, d, m = witness
            else:
                return [False, False, False, False]
        else:
            R = witness.R
            a = witness.a
            b = witness.b
            d = witness.d
            m = witness.m
    except Exception:
        return [False, False, False, False]

    # H1: R is a principal ideal domain
    try:
        h1 = False
        if hasattr(R, 'is_PID'):
            h1 = R.is_PID() if callable(R.is_PID) else bool(R.is_PID)
        elif hasattr(R, 'is_PrincipalIdealDomain'):
            h1 = R.is_PrincipalIdealDomain() if callable(R.is_PrincipalIdealDomain) else bool(R.is_PrincipalIdealDomain)
        else:
            from sympy import ZZ
            from sympy.polys.domains import PolynomialRing
            if R == ZZ:
                h1 = True
            elif isinstance(R, PolynomialRing) and R.domain.is_Field and len(R.gens) == 1:
                h1 = True
    except Exception:
        h1 = False

    # H2: d is a greatest common divisor of a and b
    try:
        h2 = False
        if divides(d, a, R) and divides(d, b, R):
            if hasattr(R, 'gcd'):
                true_gcd = R.gcd(a, b)
                h2 = is_associate(d, true_gcd, R)
            else:
                from sympy import ZZ
                if R == ZZ or str(R) == 'ZZ':
                    true_gcd = math.gcd(int(a), int(b))
                    h2 = is_associate(d, true_gcd, R)
    except Exception:
        h2 = False

    # H3: m is a least common multiple of a and b
    try:
        h3 = False
        if divides(a, m, R) and divides(b, m, R):
            if hasattr(R, 'lcm'):
                true_lcm = R.lcm(a, b)
                h3 = is_associate(m, true_lcm, R)
            else:
                from sympy import ZZ
                if R == ZZ or str(R) == 'ZZ':
                    true_lcm = abs(int(a)*int(b)) // math.gcd(int(a), int(b)) if (a and b) else 0
                    h3 = is_associate(m, true_lcm, R)
    except Exception:
        h3 = False

    # neg_Q: The product ab is NOT associate to the product dm in R
    try:
        if hasattr(R, 'mul'):
            ab = R.mul(a, b)
            dm = R.mul(d, m)
        else:
            ab = a * b
            dm = d * m
        neg_q = not is_associate(ab, dm, R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: d is a greatest common divisor of a and b",
    "H_3: m is a least common multiple of a and b",
    "¬Q: The product ab is not associate to the product dm in R"
]

N_HYP = 3
NEG_Q_INDEX = 3