import sympy
from sympy import Poly, Symbol
from sympy.polys.domains import QQ, GF

# Top-level setup
# The witness can be a tuple (n, a) assuming the field is QQ,
# or a tuple (domain, n, a) specifying a sympy field domain like QQ or GF(p).

def conditions(witness):
    try:
        if len(witness) == 2:
            domain = QQ
            n, a = witness
        elif len(witness) == 3:
            domain, n, a = witness
        else:
            return [False, False, False]
            
        if not getattr(domain, 'is_Field', False):
            return [False, False, False]
            
        if not isinstance(n, (int, sympy.Integer)) or n <= 1:
            return [False, False, False]
        n = int(n)
            
        a = domain.convert(a)
    except Exception:
        return [False, False, False]

    # H1: Assume the characteristic of F does not divide n
    try:
        char = domain.characteristic
        if char == 0:
            h1 = True
        else:
            h1 = (n % char != 0)
    except Exception:
        h1 = False

    # H2: Let a in F be an element that is not a d-th power in F for any divisor d > 1 of n
    try:
        h2 = True
        x = Symbol('x')
        for d in range(2, n + 1):
            if n % d == 0:
                poly = Poly(x**d - a, x, domain=domain)
                # If there are any roots in the ground domain, a is a d-th power
                roots = poly.ground_roots()
                if roots:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The polynomial x^n - a is NOT irreducible over F
    try:
        x = Symbol('x')
        poly = Poly(x**n - a, x, domain=domain)
        factors = poly.factor_list()[1]
        # The polynomial is irreducible if it has exactly 1 factor and its multiplicity is 1
        is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: characteristic of F does not divide n",
    "H_2: a is not a d-th power in F for any divisor d > 1 of n",
    "¬Q: x^n - a is reducible over F"
]

N_HYP = 2
NEG_Q_INDEX = 2