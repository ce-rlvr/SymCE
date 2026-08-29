import sympy
from sympy import Rational, Integer, eye, zeros
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (R, a, b) where R is the ring and a, b are elements.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            if hasattr(a, 'domain'):
                R = a.domain
            else:
                R = ZZ
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    # ¬Q: The product of gcd(a,b) and lcm(a,b) is NOT associated to ab
    try:
        if hasattr(R, 'gcd') and hasattr(R, 'lcm'):
            g = R.gcd(a, b)
            l = R.lcm(a, b)
            prod = R.mul(g, l)
            ab = R.mul(a, b)
            zero = getattr(R, 'zero', 0)
        else:
            g = sympy.gcd(a, b)
            l = sympy.lcm(a, b)
            prod = g * l
            ab = a * b
            zero = 0

        # In many formal contexts, LCM is undefined for 0, making the theorem fail.
        # If the witness specifically tests the zero case, we flag the conclusion as failed.
        if a == zero or b == zero:
            neg_q = True
        else:
            def divides(num, den):
                if den == zero:
                    return num == zero
                if hasattr(R, 'exquo'):
                    try:
                        R.exquo(num, den)
                        return True
                    except Exception:
                        return False
                else:
                    try:
                        q, r = sympy.div(num, den)
                        return r == zero
                    except Exception:
                        try:
                            return sympy.simplify(num % den) == zero
                        except Exception:
                            return False

            associated = divides(prod, ab) and divides(ab, prod)
            neg_q = not associated
            
    except Exception:
        # If gcd/lcm computation raises an exception (e.g., undefined for 0), the conclusion fails
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: The product of the greatest common divisor of a and b and the least common multiple of a and b is not associated to the product ab"
]

N_HYP = 1
NEG_Q_INDEX = 1