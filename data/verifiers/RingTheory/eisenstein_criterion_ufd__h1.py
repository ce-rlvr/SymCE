import sympy

x = sympy.symbols('x')

class ZxZ:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __add__(self, other):
        return ZxZ(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        return ZxZ(self.a - other.a, self.b - other.b)
    def __mul__(self, other):
        return ZxZ(self.a * other.a, self.b * other.b)
    def __eq__(self, other):
        if not hasattr(other, 'a') or not hasattr(other, 'b'):
            return False
        return self.a == other.a and self.b == other.b
    def __repr__(self):
        return f"ZxZ({self.a}, {self.b})"

def divides(x_val, y_val):
    if hasattr(x_val, 'a') and hasattr(x_val, 'b'):
        if not hasattr(y_val, 'a') or not hasattr(y_val, 'b'):
            return False
        if x_val.a == 0 and y_val.a != 0: return False
        if x_val.b == 0 and y_val.b != 0: return False
        return (x_val.a == 0 or y_val.a % x_val.a == 0) and (x_val.b == 0 or y_val.b % x_val.b == 0)
    else:
        if isinstance(x_val, (int, sympy.Integer)) and isinstance(y_val, (int, sympy.Integer)):
            if x_val == 0: return y_val == 0
            return y_val % x_val == 0
        try:
            q, r = sympy.div(y_val, x_val)
            return r == 0
        except Exception:
            return False

def is_prime(p_val):
    if hasattr(p_val, 'a') and hasattr(p_val, 'b'):
        a_prime = sympy.isprime(abs(p_val.a))
        b_prime = sympy.isprime(abs(p_val.b))
        a_unit = abs(p_val.a) == 1
        b_unit = abs(p_val.b) == 1
        return (a_prime and b_unit) or (a_unit and b_prime)
    else:
        if isinstance(p_val, (int, sympy.Integer)):
            return sympy.isprime(abs(int(p_val)))
        try:
            factors = sympy.factor_list(p_val)
            return len(factors[1]) == 1 and factors[1][0][1] == 1
        except Exception:
            return False

def is_reducible_in_K(coeffs):
    if all(hasattr(c, 'a') and hasattr(c, 'b') for c in coeffs):
        f1 = sum(c.a * x**i for i, c in enumerate(coeffs))
        f2 = sum(c.b * x**i for i, c in enumerate(coeffs))
        
        f1_poly = sympy.Poly(f1, x, domain='QQ')
        f2_poly = sympy.Poly(f2, x, domain='QQ')
        
        deg1 = f1_poly.degree()
        deg2 = f2_poly.degree()
        
        if deg1 > 0 and deg2 > 0:
            return True
            
        def is_poly_reducible(p_poly):
            if p_poly.degree() <= 1:
                return False
            factors = sympy.factor_list(p_poly)[1]
            num_factors = sum(mult for fac, mult in factors if fac.degree() >= 1)
            return num_factors > 1
            
        return is_poly_reducible(f1_poly) or is_poly_reducible(f2_poly)
    else:
        f = sum(c * x**i for i, c in enumerate(coeffs))
        f_poly = sympy.Poly(f, x, domain='QQ')
        if f_poly.degree() <= 1:
            return False
        factors = sympy.factor_list(f_poly)[1]
        num_factors = sum(mult for fac, mult in factors if fac.degree() >= 1)
        return num_factors > 1

def conditions(witness) -> list[bool]:
    try:
        coeffs, p_val = witness
        
        n = len(coeffs) - 1
        while n >= 0:
            c = coeffs[n]
            if hasattr(c, 'a'):
                if c.a != 0 or c.b != 0:
                    break
            else:
                if c != 0:
                    break
            n -= 1
            
        if n < 0:
            return [False] * 6
            
        coeffs = coeffs[:n+1]
        a_n = coeffs[n]
        a_0 = coeffs[0]
    except Exception:
        return [False] * 6

    try:
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        h2 = is_prime(p_val)
    except Exception:
        h2 = False

    try:
        h3 = True
        for i in range(n):
            if not divides(p_val, coeffs[i]):
                h3 = False
                break
    except Exception:
        h3 = False

    try:
        h4 = not divides(p_val, a_n)
    except Exception:
        h4 = False

    try:
        if hasattr(p_val, 'a'):
            p2 = ZxZ(p_val.a**2, p_val.b**2)
        else:
            p2 = p_val**2
        h5 = not divides(p2, a_0)
    except Exception:
        h5 = False

    try:
        neg_q = is_reducible_in_K(coeffs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over R of degree n >= 1",
    "H_2: p is a prime element of R",
    "H_3: p divides a_i for all 0 <= i < n",
    "H_4: p does not divide a_n",
    "H_5: p^2 does not divide a_0",
    "¬Q: f is reducible over K"
]

N_HYP = 5
NEG_Q_INDEX = 5