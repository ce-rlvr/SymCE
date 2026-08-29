import sympy
from sympy import Poly, Symbol, QQ, ZZ, RR, CC, I, pi, E

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    witness: tuple (F, p, a)
    F: sympy Domain (e.g., sympy.QQ)
    p: int (prime number)
    a: sympy Expr (element to check)
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        F, p, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(sympy.isprime(p))
    except Exception:
        h2 = False
        
    # H_3: There does not exist any element c in F such that c**p == a
    try:
        # Check if 'a' is an element of the field F
        try:
            F.from_sympy(sympy.sympify(a))
            is_in_F = True
        except Exception:
            is_in_F = False

        if not is_in_F:
            # If 'a' is not in F, then no element c in F can satisfy c**p == a
            # because c in F implies c**p in F, but a is not in F.
            h3 = True
        else:
            x_sym = Symbol('x')
            # Find roots of x**p - a in F
            rts = sympy.roots(x_sym**p - a, x_sym, domain=F)
            h3 = bool(len(rts) == 0)
    except Exception:
        h3 = False
        
    # neg_Q: The polynomial x**p - a is NOT irreducible over F
    try:
        try:
            F.from_sympy(sympy.sympify(a))
            is_in_F = True
        except Exception:
            is_in_F = False

        if not is_in_F:
            # If 'a' is not in F, then x**p - a is not a polynomial in F[x],
            # so it cannot be irreducible over F.
            neg_q = True
        else:
            x_sym = Symbol('x')
            poly = Poly(x_sym**p - a, x_sym, domain=F)
            neg_q = bool(not poly.is_irreducible)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is a prime number",
    "H_3: There does not exist any element c in F such that c**p == a",
    "¬Q: The polynomial x**p - a is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3