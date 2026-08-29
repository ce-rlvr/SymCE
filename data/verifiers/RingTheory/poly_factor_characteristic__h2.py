import sympy
from sympy import Poly, groebner
from sympy.abc import x
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity having characteristic n > 0",
    "neg_Q: The characteristic of the polynomial factor ring is not equal to n"
]

def get_char(n, f_expr):
    """
    Computes the characteristic of Z_n[x]/<f(x)>.
    The characteristic is the smallest positive integer k such that k is in the ideal <f(x), n> in Z[x].
    """
    try:
        f_sym = sympy.sympify(f_expr)
        p = Poly(f_sym, x, domain='ZZ')
        if p.degree() <= 0:
            if p.is_zero:
                return n
            a = int(p.as_expr())
            return math.gcd(abs(a), n)
    except Exception:
        pass

    try:
        # Compute Groebner basis of the ideal <f(x), n> in Z[x]
        gb = groebner([f_sym, n], x, domain='ZZ')
        c = n
        for expr in gb:
            p = Poly(expr, x)
            # If the polynomial is a constant, it belongs to the elimination ideal in Z
            if p.degree() == 0:
                val = abs(int(p.as_expr()))
                if val > 0:
                    c = math.gcd(c, val)
        return c
    except Exception:
        return n

def conditions(witness):
    try:
        n, f_expr = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(n, int) and n > 0
        if h1:
            f_sym = sympy.sympify(f_expr)
            # Ensure the expression only contains the variable x (or is a constant)
            if not f_sym.free_symbols.issubset({x}):
                h1 = False
            else:
                # Ensure all coefficients are integers (so it's a valid polynomial in Z_n[x])
                p = Poly(f_sym, x, domain='ZZ')
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            char_val = get_char(n, f_expr)
            neg_q = bool(char_val != n)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]