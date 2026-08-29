import sympy
from sympy import Symbol, Poly, isprime, GF, QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z, t

# Top-level setup: common fields that might be referenced in a witness
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)
F7 = GF(7)

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p > 0",
    "H_2: There does not exist any element c in F such that c^p - c = a",
    "¬Q: The polynomial x^p - x - a is not irreducible over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    F, p, a = None, None, None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, p, a = witness
            elif len(witness) == 2:
                if hasattr(witness[0], 'characteristic'):
                    F, a = witness
                    p = F.characteristic()
                else:
                    p, a = witness
                    F = GF(p)
        elif isinstance(witness, dict):
            F = witness.get('F')
            p = witness.get('p')
            a = witness.get('a')
    except Exception:
        pass

    # H_1: F is a field of prime characteristic p > 0
    try:
        h1 = False
        if F is not None and p is not None:
            if getattr(F, 'is_Field', False) or getattr(F, 'is_field', False):
                c = getattr(F, 'characteristic', lambda: 0)()
                if c == p and p > 0 and isprime(p):
                    h1 = True
    except Exception:
        h1 = False

    # H_2: There does not exist any element c in F such that c^p - c = a
    try:
        h2 = True
        if F is not None and p is not None and a is not None:
            try:
                a_F = F(a)
                a_in_F = True
            except Exception:
                a_in_F = False

            if a_in_F:
                X = Symbol('X')
                poly = Poly(X**p - X - a_F, X, domain=F)
                # If there are any roots in F, then such an element c exists
                if poly.ground_roots():
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The polynomial x^p - x - a is NOT irreducible over F
    try:
        neg_q = False
        if F is not None and p is not None and a is not None:
            try:
                a_F = F(a)
                a_in_F = True
            except Exception:
                a_in_F = False

            if not a_in_F:
                # If a is not in F, x^p - x - a is not a valid polynomial over F,
                # hence it cannot be irreducible over F.
                neg_q = True
            else:
                X = Symbol('X')
                try:
                    poly = Poly(X**p - X - a_F, X, domain=F)
                    is_irred = poly.is_irreducible
                    neg_q = not is_irred
                except Exception:
                    # If irreducibility check fails, default to False to avoid false positives
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]