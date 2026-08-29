import sympy
import math

class Z_sqrt_minus_5:
    """
    Represents an element a + b*sqrt(-5) in the ring Z[sqrt(-5)].
    This ring is a standard example of a domain that is not a UFD.
    """
    def __init__(self, a, b=0):
        self.a = int(a)
        self.b = int(b)

    def _to_Z(self, other):
        if isinstance(other, Z_sqrt_minus_5):
            return other
        if isinstance(other, (int, sympy.Integer)):
            return Z_sqrt_minus_5(int(other))
        return NotImplemented

    def __add__(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return NotImplemented
        return Z_sqrt_minus_5(self.a + other.a, self.b + other.b)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return NotImplemented
        return Z_sqrt_minus_5(self.a - other.a, self.b - other.b)

    def __rsub__(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return NotImplemented
        return Z_sqrt_minus_5(other.a - self.a, other.b - self.b)

    def __mul__(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return NotImplemented
        return Z_sqrt_minus_5(self.a * other.a - 5 * self.b * other.b,
                              self.a * other.b + self.b * other.a)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return False
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        return f"{self.a} + {self.b}*sqrt(-5)"

    def __repr__(self):
        return self.__str__()

    def norm(self):
        return self.a**2 + 5 * self.b**2

    def divides(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return False
        if self.a == 0 and self.b == 0:
            return other.a == 0 and other.b == 0
        n = self.norm()
        if n == 0:
            return False
        real_num = other.a * self.a + 5 * other.b * self.b
        imag_num = other.b * self.a - other.a * self.b
        return real_num % n == 0 and imag_num % n == 0

    def divisors(self):
        n = self.norm()
        if n == 0:
            return set()
        divs = set()
        for i in range(1, int(math.isqrt(n)) + 1):
            if n % i == 0:
                possible_norms = {i, n // i}
                for norm in possible_norms:
                    max_b = int(math.isqrt(norm // 5))
                    for b in range(-max_b, max_b + 1):
                        rem = norm - 5 * b**2
                        if rem >= 0:
                            a = int(math.isqrt(rem))
                            if a * a == rem:
                                d1 = Z_sqrt_minus_5(a, b)
                                if d1.divides(self):
                                    divs.add(d1)
                                d2 = Z_sqrt_minus_5(-a, b)
                                if d2.divides(self):
                                    divs.add(d2)
        return divs

    def is_coprime(self, other):
        other = self._to_Z(other)
        if other is NotImplemented: return False
        if self.norm() == 0:
            return other.norm() == 1
        if other.norm() == 0:
            return self.norm() == 1
        divs_self = self.divisors()
        divs_other = other.divisors()
        common = divs_self.intersection(divs_other)
        for d in common:
            if d.norm() != 1:
                return False
        return True

# Top-level setup bindings
sqrt_minus_5 = Z_sqrt_minus_5(0, 1)

def to_ring_element(x):
    if isinstance(x, Z_sqrt_minus_5):
        return x
    if isinstance(x, (int, sympy.Integer)):
        return Z_sqrt_minus_5(int(x))
    try:
        if hasattr(x, 'free_symbols'):
            x_exp = sympy.expand(x)
            s = sympy.sqrt(5)*sympy.I
            a = sympy.expand(x_exp.subs(s, 0))
            b = sympy.expand((x_exp - a) / s)
            if a.is_Integer and b.is_Integer:
                return Z_sqrt_minus_5(int(a), int(b))
    except Exception:
        pass
    return x

def conditions(witness):
    try:
        if len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            a, b, c = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        a = to_ring_element(a)
        b = to_ring_element(b)
        c = to_ring_element(c)
    except Exception:
        pass

    def is_zero(x):
        if isinstance(x, Z_sqrt_minus_5):
            return x.a == 0 and x.b == 0
        if hasattr(x, 'is_zero'):
            return x.is_zero == True
        return x == 0

    def check_coprime(x, y):
        if isinstance(x, Z_sqrt_minus_5) and isinstance(y, Z_sqrt_minus_5):
            return x.is_coprime(y)
        try:
            return sympy.gcd(x, y) == 1
        except Exception:
            return False

    try:
        h1 = not is_zero(a) and not is_zero(b) and not is_zero(c)
    except Exception:
        h1 = False

    try:
        h2 = check_coprime(a, b)
    except Exception:
        h2 = False

    try:
        h3 = check_coprime(a, c)
    except Exception:
        h3 = False

    try:
        bc = b * c
        neg_q = not check_coprime(a, bc)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements of R",
    "H_2: a is coprime to b",
    "H_3: a is coprime to c",
    "¬Q: a is not coprime to the product bc"
]

N_HYP = 3
NEG_Q_INDEX = 3