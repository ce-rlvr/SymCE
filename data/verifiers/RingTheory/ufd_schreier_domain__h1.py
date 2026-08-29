import sympy
import math
from sympy.abc import x, y, z, w

# --- Top-level setup: Ring definitions for potential counterexamples ---

class Z_sqrt_minus_5:
    """Elements of the ring Z[sqrt(-5)]"""
    def __init__(self, re, im=0):
        self.re = int(re)
        self.im = int(im)
        
    def __add__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_sqrt_minus_5(other, 0)
        return Z_sqrt_minus_5(self.re + other.re, self.im + other.im)
        
    def __radd__(self, other):
        return self.__add__(other)
        
    def __sub__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_sqrt_minus_5(other, 0)
        return Z_sqrt_minus_5(self.re - other.re, self.im - other.im)
        
    def __rsub__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_sqrt_minus_5(other, 0)
        return other.__sub__(self)
        
    def __mul__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_sqrt_minus_5(other, 0)
        return Z_sqrt_minus_5(self.re * other.re - 5 * self.im * other.im,
                              self.re * other.im + self.im * other.re)
                              
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __eq__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_sqrt_minus_5(other, 0)
        if not isinstance(other, Z_sqrt_minus_5):
            return False
        return self.re == other.re and self.im == other.im
        
    def __hash__(self):
        return hash((self.re, self.im))
        
    def norm(self):
        return self.re**2 + 5 * self.im**2
        
    def is_zero(self):
        return self.re == 0 and self.im == 0
        
    def divides(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_sqrt_minus_5(other, 0)
        if self.is_zero():
            return other.is_zero()
        n = self.norm()
        if n == 0:
            return False
        re_part = other.re * self.re + 5 * other.im * self.im
        im_part = other.im * self.re - other.re * self.im
        return re_part % n == 0 and im_part % n == 0
        
    def get_divisors(self):
        if self.is_zero():
            raise ValueError("Cannot get all divisors of zero in an infinite ring")
        n = self.norm()
        divs = []
        max_x = int(math.sqrt(n))
        max_y = int(math.sqrt(n / 5.0)) if n >= 5 else 0
        for i in range(-max_x - 1, max_x + 2):
            for j in range(-max_y - 1, max_y + 2):
                d = Z_sqrt_minus_5(i, j)
                if not d.is_zero() and d.divides(self):
                    divs.append(d)
        return divs
        
    def __repr__(self):
        return f"Z_sqrt_minus_5({self.re}, {self.im})"


class Z_n:
    """Elements of the finite ring Z_n"""
    def __init__(self, val, n):
        self.val = int(val) % int(n)
        self.n = int(n)
        
    def __add__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_n(other, self.n)
        return Z_n(self.val + other.val, self.n)
        
    def __radd__(self, other):
        return self.__add__(other)
        
    def __sub__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_n(other, self.n)
        return Z_n(self.val - other.val, self.n)
        
    def __rsub__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_n(other, self.n)
        return other.__sub__(self)
        
    def __mul__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_n(other, self.n)
        return Z_n(self.val * other.val, self.n)
        
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __eq__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_n(other, self.n)
        if not isinstance(other, Z_n):
            return False
        return self.val == other.val and self.n == other.n
        
    def is_zero(self):
        return self.val == 0
        
    def divides(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z_n(other, self.n)
        for k in range(self.n):
            if (k * self.val) % self.n == other.val:
                return True
        return False
        
    def get_divisors(self):
        divs = []
        for k in range(self.n):
            d = Z_n(k, self.n)
            if d.divides(self):
                divs.append(d)
        return divs
        
    def __repr__(self):
        return f"Z_n({self.val}, {self.n})"


class Z2_X_Y_mod_m2:
    """Elements of the finite local ring Z_2[X, Y] / (X^2, XY, Y^2)"""
    def __init__(self, c0, cX, cY):
        self.c0 = int(c0) % 2
        self.cX = int(cX) % 2
        self.cY = int(cY) % 2
        
    def __add__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z2_X_Y_mod_m2(other, 0, 0)
        return Z2_X_Y_mod_m2(self.c0 + other.c0, self.cX + other.cX, self.cY + other.cY)
        
    def __radd__(self, other):
        return self.__add__(other)
        
    def __sub__(self, other):
        return self.__add__(other)
        
    def __rsub__(self, other):
        return self.__add__(other)
        
    def __mul__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z2_X_Y_mod_m2(other, 0, 0)
        return Z2_X_Y_mod_m2(self.c0 * other.c0,
                             self.c0 * other.cX + self.cX * other.c0,
                             self.c0 * other.cY + self.cY * other.c0)
                             
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __eq__(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z2_X_Y_mod_m2(other, 0, 0)
        if not isinstance(other, Z2_X_Y_mod_m2):
            return False
        return self.c0 == other.c0 and self.cX == other.cX and self.cY == other.cY
        
    def is_zero(self):
        return self.c0 == 0 and self.cX == 0 and self.cY == 0
        
    def divides(self, other):
        if isinstance(other, (int, sympy.Integer)):
            other = Z2_X_Y_mod_m2(other, 0, 0)
        for d0 in range(2):
            for dX in range(2):
                for dY in range(2):
                    k = Z2_X_Y_mod_m2(d0, dX, dY)
                    if (self * k) == other:
                        return True
        return False
        
    def get_divisors(self):
        divs = []
        for d0 in range(2):
            for dX in range(2):
                for dY in range(2):
                    d = Z2_X_Y_mod_m2(d0, dX, dY)
                    if d.divides(self):
                        divs.append(d)
        return divs
        
    def __repr__(self):
        return f"Z2_X_Y_mod_m2({self.c0}, {self.cX}, {self.cY})"


# --- Helper functions for the verifier ---

def convert_to_ring_element(val):
    if hasattr(val, 'divides'):
        return val
    if isinstance(val, (int, sympy.Integer)):
        return val
    try:
        a = sympy.re(val)
        b = sympy.im(val) / sympy.sqrt(5)
        try:
            a_val = int(a)
            b_val = int(b)
            if sympy.simplify(a - a_val) == 0 and sympy.simplify(b - b_val) == 0:
                return Z_sqrt_minus_5(a_val, b_val)
        except Exception:
            pass
    except Exception:
        pass
    return val

def get_divisors(x):
    if hasattr(x, 'get_divisors'):
        return x.get_divisors()
    if isinstance(x, (int, sympy.Integer)):
        x_val = int(x)
        if x_val == 0:
            raise ValueError("Cannot get all divisors of zero in Z")
        divs = []
        for i in range(1, abs(x_val) + 1):
            if x_val % i == 0:
                divs.append(i)
                divs.append(-i)
        return divs
    raise ValueError("Unsupported type for get_divisors")

def divides(x, y):
    if hasattr(x, 'divides'):
        return x.divides(y)
    if isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)):
        x_val = int(x)
        y_val = int(y)
        if x_val == 0:
            return y_val == 0
        return y_val % x_val == 0
    raise ValueError("Unsupported type for divides")

def is_zero(x):
    if hasattr(x, 'is_zero'):
        return x.is_zero()
    if isinstance(x, (int, sympy.Integer)):
        return int(x) == 0
    raise ValueError("Unsupported type for is_zero")

def mul(x, y):
    return x * y


# --- Verifier Module ---

def conditions(witness) -> list[bool]:
    try:
        w = list(witness)
    except Exception:
        return [False, False, False]
    
    if len(w) != 3:
        return [False, False, False]

    try:
        for i in range(3):
            w[i] = convert_to_ring_element(w[i])
        
        # Unify types if mixed with integers
        if any(isinstance(val, Z_sqrt_minus_5) for val in w):
            for i in range(3):
                if isinstance(w[i], (int, sympy.Integer)):
                    w[i] = Z_sqrt_minus_5(int(w[i]), 0)
        elif any(isinstance(val, Z_n) for val in w):
            n = next(val.n for val in w if isinstance(val, Z_n))
            for i in range(3):
                if isinstance(w[i], (int, sympy.Integer)):
                    w[i] = Z_n(int(w[i]), n)
        elif any(isinstance(val, Z2_X_Y_mod_m2) for val in w):
            for i in range(3):
                if isinstance(w[i], (int, sympy.Integer)):
                    w[i] = Z2_X_Y_mod_m2(int(w[i]), 0, 0)
                    
        a, b, c = w
    except Exception:
        return [False, False, False]

    # H_1: a, b, c are non-zero elements of R
    try:
        h1 = not is_zero(a) and not is_zero(b) and not is_zero(c)
    except Exception:
        h1 = False

    # H_2: a divides the product bc
    try:
        bc = mul(b, c)
        h2 = divides(a, bc)
    except Exception:
        h2 = False

    # ¬Q: For all a1, a2 in R, not (a = a1 a2 and a1 | b and a2 | c)
    try:
        neg_q = True
        divs = get_divisors(a)
        for a1 in divs:
            for a2 in divs:
                if mul(a1, a2) == a:
                    if divides(a1, b) and divides(a2, c):
                        neg_q = False
                        break
            if not neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero elements of R",
    "H_2: a divides the product bc",
    "¬Q: There do not exist a1, a2 in R such that a = a1 a2, a1 | b, and a2 | c"
]

N_HYP = 2
NEG_Q_INDEX = 2