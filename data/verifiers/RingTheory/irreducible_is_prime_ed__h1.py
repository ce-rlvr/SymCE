import sympy
from sympy.abc import x, y, z
import math
import itertools

# Top-level setup: Define standard counterexample rings and elements.
# The conjecture states that irreducible elements are prime. This is true in UFDs,
# but false in general rings (e.g., Z[sqrt(-5)] or certain finite rings).

class Z_sqrt_minus_5:
    """
    Represents an element a + b*sqrt(-5) in the Dedekind domain Z[sqrt(-5)].
    This is the standard infinite ring counterexample.
    """
    def __init__(self, a, b):
        self.a = int(a)
        self.b = int(b)

    def __eq__(self, other):
        if isinstance(other, Z_sqrt_minus_5):
            return self.a == other.a and self.b == other.b
        if isinstance(other, (int, float, sympy.Integer, sympy.Float)):
            return self.a == other and self.b == 0
        return False

    def __add__(self, other):
        if isinstance(other, (int, float, sympy.Integer, sympy.Float)):
            other = Z_sqrt_minus_5(other, 0)
        return Z_sqrt_minus_5(self.a + other.a, self.b + other.b)

    def __mul__(self, other):
        if isinstance(other, (int, float, sympy.Integer, sympy.Float)):
            other = Z_sqrt_minus_5(other, 0)
        return Z_sqrt_minus_5(self.a * other.a - 5 * self.b * other.b,
                              self.a * other.b + self.b * other.a)

    def norm(self):
        return self.a**2 + 5 * self.b**2

    def is_unit(self):
        return self.norm() == 1

    def divides(self, other):
        if isinstance(other, (int, float, sympy.Integer, sympy.Float)):
            other = Z_sqrt_minus_5(other, 0)
        if self.norm() == 0:
            return other.norm() == 0
        if other.norm() % self.norm() != 0:
            return False
        N = self.norm()
        real_part = other.a * self.a + 5 * other.b * self.b
        imag_part = other.b * self.a - other.a * self.b
        return real_part % N == 0 and imag_part % N == 0

    def is_irreducible(self):
        if self.norm() <= 1:
            return False
        N = self.norm()
        for i in range(2, int(math.isqrt(N)) + 1):
            if N % i == 0:
                for elem in self._elements_of_norm(i):
                    if elem.divides(self):
                        return False
        return True

    @staticmethod
    def _elements_of_norm(n):
        elements = []
        for b in range(int(math.isqrt(n // 5)) + 1):
            a2 = n - 5 * b**2
            if a2 < 0:
                continue
            a = int(math.isqrt(a2))
            if a**2 == a2:
                elements.append(Z_sqrt_minus_5(a, b))
                if a != 0:
                    elements.append(Z_sqrt_minus_5(-a, b))
                if b != 0:
                    elements.append(Z_sqrt_minus_5(a, -b))
                if a != 0 and b != 0:
                    elements.append(Z_sqrt_minus_5(-a, -b))
        return elements

    def is_prime(self):
        if self.norm() <= 1:
            return False
        N = self.norm()
        if sympy.isprime(N):
            return True
        if self.b == 0 and self.a != 0:
            q = abs(self.a)
            if sympy.isprime(q):
                if q == 2 or q == 5:
                    return False
                if sympy.jacobi_symbol(-5, q) == -1:
                    return True
        return False


class FiniteRingElement:
    """
    Represents an element in a finite ring.
    """
    def __init__(self, ring, val):
        self.ring = ring
        self.val = val

    def __eq__(self, other):
        if not isinstance(other, FiniteRingElement):
            return False
        return self.val == other.val

    def __add__(self, other):
        return FiniteRingElement(self.ring, self.ring.add(self.val, other.val))

    def __mul__(self, other):
        return FiniteRingElement(self.ring, self.ring.mul(self.val, other.val))

    def is_unit(self):
        return self.ring.is_unit(self.val)

    def divides(self, other):
        return self.ring.divides(self.val, other.val)

    def is_irreducible(self):
        return self.ring.is_irreducible(self.val)

    def is_prime(self):
        return self.ring.is_prime(self.val)


class FiniteRing:
    """
    A generic finite ring checker.
    """
    def __init__(self, elements, add_func, mul_func, zero_val, one_val):
        self.elements = elements
        self.add_func = add_func
        self.mul_func = mul_func
        self.zero_val = zero_val
        self.one_val = one_val

    def add(self, a, b):
        return self.add_func(a, b)

    def mul(self, a, b):
        return self.mul_func(a, b)

    def is_unit(self, x):
        for y in self.elements:
            if self.mul(x, y) == self.one_val:
                return True
        return False

    def divides(self, a, b):
        for c in self.elements:
            if self.mul(a, c) == b:
                return True
        return False

    def is_irreducible(self, p):
        if p == self.zero_val or self.is_unit(p):
            return False
        for a in self.elements:
            for b in self.elements:
                if self.mul(a, b) == p:
                    if not (self.is_unit(a) or self.is_unit(b)):
                        return False
        return True

    def is_prime(self, p):
        if p == self.zero_val or self.is_unit(p):
            return False
        for a in self.elements:
            for b in self.elements:
                ab = self.mul(a, b)
                if self.divides(p, ab):
                    if not (self.divides(p, a) or self.divides(p, b)):
                        return False
        return True


# A finite ring counterexample: F_2[x, y] / (x^2, xy, y^2)
_R_elements = list(itertools.product([0, 1], repeat=3))
def _R_add(u, v):
    return (u[0]^v[0], u[1]^v[1], u[2]^v[2])
def _R_mul(u, v):
    return (u[0]*v[0], (u[0]*v[1] + u[1]*v[0])%2, (u[0]*v[2] + u[2]*v[0])%2)

R_counterexample = FiniteRing(_R_elements, _R_add, _R_mul, (0,0,0), (1,0,0))
x_elem = FiniteRingElement(R_counterexample, (0, 1, 0))
y_elem = FiniteRingElement(R_counterexample, (0, 0, 1))


def conditions(witness) -> list[bool]:
    # Auto-convert common formats to Z_sqrt_minus_5 if applicable
    if isinstance(witness, (int, float, sympy.Integer, sympy.Float)):
        witness = Z_sqrt_minus_5(int(witness), 0)
    elif isinstance(witness, tuple):
        if len(witness) == 2 and hasattr(witness[1], 'is_irreducible'):
            witness = witness[1]
        elif len(witness) == 2:
            try:
                witness = Z_sqrt_minus_5(int(witness[0]), int(witness[1]))
            except Exception:
                pass
    elif isinstance(witness, sympy.Expr):
        try:
            a = witness.as_coeff_add()[0]
            rest = witness - a
            if rest == 0:
                witness = Z_sqrt_minus_5(int(a), 0)
            else:
                b = rest / sympy.sqrt(-5)
                witness = Z_sqrt_minus_5(int(a), int(b))
        except Exception:
            pass

    try:
        h1 = bool(witness.is_irreducible())
    except Exception:
        h1 = False

    try:
        neg_q = not bool(witness.is_prime())
    except Exception:
        neg_q = False

    return [h1, neg_q]


CONDITION_LABELS = [
    "H_1: p is an irreducible element in R",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1