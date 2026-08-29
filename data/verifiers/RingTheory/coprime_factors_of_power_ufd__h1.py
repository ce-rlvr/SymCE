import math
import sympy as sp
from sympy import integer_nthroot

# Top-level setup
class Z_sqrt_m5:
    """
    Represents an element u + v*sqrt(-5) in the ring Z[sqrt(-5)].
    This is the standard ring used for counterexamples to this theorem.
    """
    def __init__(self, u, v):
        self.u = int(u)
        self.v = int(v)
        
    def __add__(self, other):
        if isinstance(other, int):
            return Z_sqrt_m5(self.u + other, self.v)
        if not isinstance(other, Z_sqrt_m5):
            return NotImplemented
        return Z_sqrt_m5(self.u + other.u, self.v + other.v)
        
    def __radd__(self, other):
        return self.__add__(other)
        
    def __sub__(self, other):
        if isinstance(other, int):
            return Z_sqrt_m5(self.u - other, self.v)
        if not isinstance(other, Z_sqrt_m5):
            return NotImplemented
        return Z_sqrt_m5(self.u - other.u, self.v - other.v)
        
    def __rsub__(self, other):
        if isinstance(other, int):
            return Z_sqrt_m5(other - self.u, -self.v)
        return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, int):
            return Z_sqrt_m5(self.u * other, self.v * other)
        if not isinstance(other, Z_sqrt_m5):
            return NotImplemented
        return Z_sqrt_m5(self.u * other.u - 5 * self.v * other.v,
                         self.u * other.v + self.v * other.u)
                         
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __neg__(self):
        return Z_sqrt_m5(-self.u, -self.v)
                         
    def __eq__(self, other):
        if isinstance(other, int):
            return self.u == other and self.v == 0
        if not isinstance(other, Z_sqrt_m5):
            return False
        return self.u == other.u and self.v == other.v
        
    def norm(self):
        return self.u**2 + 5 * self.v**2
        
    def is_zero(self):
        return self.u == 0 and self.v == 0
        
    def is_unit(self):
        return self.norm() == 1
        
    def divides(self, other):
        if self.is_zero():
            return False
        n = self.norm()
        conj = Z_sqrt_m5(self.u, -self.v)
        prod = other * conj
        return prod.u % n == 0 and prod.v % n == 0

    def __pow__(self, n):
        if n == 0:
            return Z_sqrt_m5(1, 0)
        res = Z_sqrt_m5(1, 0)
        base = self
        while n > 0:
            if n % 2 == 1:
                res = res * base
            base = base * base
            n //= 2
        return res
        
    def __str__(self):
        return f"{self.u} + {self.v}*sqrt(-5)"
        
    def __repr__(self):
        return f"Z_sqrt_m5({self.u}, {self.v})"

def conditions(witness):
    try:
        if hasattr(witness, 'a'):
            a_raw = witness.a
            b_raw = witness.b
            c_raw = witness.c
            n = witness.n
        else:
            a_raw, b_raw, c_raw, n = witness
    except Exception:
        return [False] * 5

    def to_elem(x):
        if isinstance(x, Z_sqrt_m5):
            return x
        if isinstance(x, tuple) and len(x) == 2:
            return Z_sqrt_m5(x[0], x[1])
        if isinstance(x, int):
            return Z_sqrt_m5(x, 0)
        return x

    try:
        a = to_elem(a_raw)
        b = to_elem(b_raw)
        c = to_elem(c_raw)
    except Exception:
        pass

    # H1: a, b, c are non-zero elements of R
    try:
        def check_not_zero(x):
            if hasattr(x, 'is_zero'):
                if callable(x.is_zero):
                    return not x.is_zero()
                else:
                    return x.is_zero is False
            return x != 0

        h1 = check_not_zero(a) and check_not_zero(b) and check_not_zero(c)
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H3: The greatest common divisor of a and b is a unit
    try:
        if hasattr(witness, 'are_coprime'):
            h3 = witness.are_coprime(a, b)
        elif hasattr(a, 'are_coprime'):
            h3 = a.are_coprime(b)
        else:
            na = a.norm()
            nb = b.norm()
            if na == 0 or nb == 0:
                h3 = False
            else:
                g = math.gcd(na, nb)
                max_v = int(math.isqrt(g // 5))
                has_non_unit_cd = False
                for v in range(-max_v - 1, max_v + 2):
                    max_u = int(math.isqrt(g))
                    for u in range(-max_u - 1, max_u + 2):
                        d = Z_sqrt_m5(u, v)
                        nd = d.norm()
                        if nd > 1 and g % nd == 0:
                            if d.divides(a) and d.divides(b):
                                has_non_unit_cd = True
                                break
                    if has_non_unit_cd:
                        break
                h3 = not has_non_unit_cd
    except Exception:
        h3 = False

    # H4: ab = c^n
    try:
        h4 = (a * b) == (c ** n)
    except Exception:
        h4 = False

    # Negated Conclusion: There do NOT exist units u, v and elements x, y such that a = u x^n and b = v y^n
    try:
        if hasattr(witness, 'is_nth_power_up_to_unit'):
            a_is_power = witness.is_nth_power_up_to_unit(a, n)
            b_is_power = witness.is_nth_power_up_to_unit(b, n)
        elif hasattr(a, 'is_nth_power_up_to_unit'):
            a_is_power = a.is_nth_power_up_to_unit(n)
            b_is_power = b.is_nth_power_up_to_unit(n)
        else:
            def is_nth_power_up_to_unit(elem, p):
                ne = elem.norm()
                if ne == 0:
                    return True
                nx, exact = integer_nthroot(ne, p)
                if not exact:
                    return False
                
                max_v = int(math.isqrt(nx // 5))
                for v in range(-max_v - 1, max_v + 2):
                    u2 = nx - 5 * v**2
                    if u2 < 0:
                        continue
                    u = int(math.isqrt(u2))
                    if u**2 == u2:
                        for sign in (1, -1):
                            x = Z_sqrt_m5(sign * u, v)
                            xp = x ** p
                            if xp == elem or xp == -elem:
                                return True
                return False

            a_is_power = is_nth_power_up_to_unit(a, n)
            b_is_power = is_nth_power_up_to_unit(b, n)
            
        neg_q = not (a_is_power and b_is_power)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements of R",
    "H_2: n is a positive integer",
    "H_3: The greatest common divisor of a and b is a unit",
    "H_4: ab = c^n",
    "¬Q: There do not exist units u, v and elements x, y such that a = u x^n and b = v y^n"
]

N_HYP = 4
NEG_Q_INDEX = 4