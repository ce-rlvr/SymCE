import sympy
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness is expected to be a tuple (p, a) or a dict {'p': p, 'a': a},
    where p is the prime characteristic and a is an element of GF(p).
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                p, a = witness
            elif len(witness) == 3:
                _, p, a = witness
            else:
                p, a = None, None
        else:
            p, a = None, None
    except Exception:
        p, a = None, None

    # H_1: K is a field of prime characteristic p > 0
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: a is an element of K
    # We accept integers as elements of the prime field GF(p)
    try:
        if p is not None and a is not None:
            h2 = isinstance(a, (int, sympy.Integer)) or (hasattr(a, 'is_integer') and a.is_integer)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The polynomial x^p - x - a is reducible over K
    try:
        if not h1 or not h2 or p > 10000:
            neg_q = False
        else:
            poly = sympy.Poly(x**p - x - int(a), x, modulus=int(p))
            neg_q = not poly.is_irreducible
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field of prime characteristic p > 0",
    "H_2: a is an element of K",
    "¬Q: The polynomial x^p - x - a is reducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2