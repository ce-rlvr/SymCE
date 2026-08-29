import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings that the witness expression may reference.
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

class Z_sqrt_minus_5:
    """
    Represents an element a + b*sqrt(-5) in the ring of integers Z[sqrt(-5)].
    This ring is a classic example of a domain that is not a Unique Factorization Domain (UFD).
    """
    def __init__(self, a, b=0):
        self.a = int(a)
        self.b = int(b)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Z_sqrt_minus_5(self.a + int(other), self.b)
        return Z_sqrt_minus_5(self.a + other.a, self.b + other.b)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Z_sqrt_minus_5(self.a - int(other), self.b)
        return Z_sqrt_minus_5(self.a - other.a, self.b - other.b)

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Z_sqrt_minus_5(int(other) - self.a, -self.b)
        return Z_sqrt_minus_5(other.a - self.a, other.b - self.b)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Z_sqrt_minus_5(self.a * int(other), self.b * int(other))
        return Z_sqrt_minus_5(self.a * other.a - 5 * self.b * other.b,
                              self.a * other.b + self.b * other.a)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Only non-negative integer powers are supported")
        res = Z_sqrt_minus_5(1, 0)
        base = self
        for _ in range(n):
            res = res * base
        return res

    def norm(self):
        return self.a**2 + 5 * self.b**2

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.a == int(other) and self.b == 0
        if not isinstance(other, Z_sqrt_minus_5):
            return False
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        elif self.a == 0:
            if self.b == 1: return "sqrt(-5)"
            if self.b == -1: return "-sqrt(-5)"
            return f"{self.b}*sqrt(-5)"
        else:
            sign = "+" if self.b > 0 else "-"
            abs_b = abs(self.b)
            b_str = f"{abs_b}*" if abs_b != 1 else ""
            return f"{self.a} {sign} {b_str}sqrt(-5)"

    def divisors(self):
        n = self.norm()
        if n == 0:
            return set()
        if n > 1000000:
            raise ValueError("Norm too large to compute divisors safely")
        divs = set()
        limit_a = int(math.isqrt(n)) + 1
        limit_b = int(math.isqrt(n // 5)) + 1
        for a in range(-limit_a, limit_a + 1):
            for b in range(-limit_b, limit_b + 1):
                cand = Z_sqrt_minus_5(a, b)
                cn = cand.norm()
                if cn == 0:
                    continue
                if n % cn == 0:
                    conj = Z_sqrt_minus_5(cand.a, -cand.b)
                    prod = self * conj
                    if prod.a % cn == 0 and prod.b % cn == 0:
                        divs.add(cand)
        return divs

def gcd_Z_sqrt_minus_5(x, y):
    if x.norm() == 0 and y.norm() == 0:
        return Z_sqrt_minus_5(0, 0)
    if x.norm() == 0:
        return y
    if y.norm() == 0:
        return x
    divs_x = x.divisors()
    divs_y = y.divisors()
    common = divs_x & divs_y
    for d in common:
        is_gcd = True
        d_divs = d.divisors()
        for c in common:
            if c not in d_divs:
                is_gcd = False
                break
        if is_gcd:
            return d
    return None

def conditions(witness):
    """
    Given a witness object, checks whether it is a valid counterexample.
    Returns a list of booleans corresponding to the hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            n = witness.get('n')
            m = witness.get('m')
        elif isinstance(witness, tuple) and len(witness) == 4:
            a, b, n, m = witness
        else:
            a = getattr(witness, 'a', None)
            b = getattr(witness, 'b', None)
            n = getattr(witness, 'n', None)
            m = getattr(witness, 'm', None)
            
        if a is None or b is None or n is None or m is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: a and b are elements of R
    try:
        h1 = True
        if isinstance(a, Z_sqrt_minus_5) and isinstance(b, Z_sqrt_minus_5):
            pass
        elif isinstance(a, (int, float, complex)) and isinstance(b, (int, float, complex)):
            pass
        elif hasattr(a, 'free_symbols'):
            pass
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: The greatest common divisor of a and b is a unit in R
    try:
        if isinstance(a, Z_sqrt_minus_5) and isinstance(b, Z_sqrt_minus_5):
            g = gcd_Z_sqrt_minus_5(a, b)
            h2 = g is not None and g.norm() == 1
        elif hasattr(a, 'gcd') and hasattr(a, 'is_unit'):
            g = a.gcd(b)
            h2 = g.is_unit()
        else:
            g = sympy.gcd(a, b)
            h2 = g in [1, -1, sympy.S.One, sympy.S.NegativeOne]
    except Exception:
        h2 = False

    # H3: n and m are positive integers
    try:
        h3 = isinstance(n, int) and n > 0 and isinstance(m, int) and m > 0
    except Exception:
        h3 = False

    # ¬Q: The greatest common divisor of a^n and b^m is NOT a unit in R
    try:
        an = a**n
        bm = b**m
        if isinstance(a, Z_sqrt_minus_5) and isinstance(b, Z_sqrt_minus_5):
            g_ab = gcd_Z_sqrt_minus_5(an, bm)
            is_unit_ab = g_ab is not None and g_ab.norm() == 1
        elif hasattr(an, 'gcd') and hasattr(an, 'is_unit'):
            g_ab = an.gcd(bm)
            is_unit_ab = g_ab.is_unit()
        else:
            g_ab = sympy.gcd(an, bm)
            is_unit_ab = g_ab in [1, -1, sympy.S.One, sympy.S.NegativeOne]
        neg_q = not is_unit_ab
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "H_2: The greatest common divisor of a and b is a unit in R",
    "H_3: n and m are positive integers",
    "¬Q: The greatest common divisor of a^n and b^m is NOT a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3