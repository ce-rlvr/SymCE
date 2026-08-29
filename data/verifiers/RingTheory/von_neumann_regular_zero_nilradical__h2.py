import sympy
from sympy.abc import x, y, z
from sympy import QQ, ZZ, Rational, Integer

def conditions(witness) -> list[bool]:
    def _is_int_ring(w):
        if isinstance(w, int):
            return True
        if hasattr(w, 'is_integer'):
            if callable(w.is_integer):
                return w.is_integer()
            return w.is_integer
        return False

    def _is_square_free(n):
        # A simple square-free check for integers
        n = abs(int(n))
        if n == 0:
            return False
        if n == 1:
            return True
        for p, e in sympy.factorint(n).items():
            if e > 1:
                return False
        return True

    # H_1: R is a commutative ring
    try:
        if _is_int_ring(witness):
            n = abs(int(witness))
            h1_ok = n >= 0
        else:
            h1_ok = getattr(witness, 'is_commutative', False)
    except Exception:
        h1_ok = False

    # neg_Q: The nilradical of R is not the zero ideal
    try:
        if _is_int_ring(witness):
            n = abs(int(witness))
            if n == 0 or n == 1:
                neg_q_ok = False
            else:
                # In Z/nZ, the nilradical is non-zero iff n is not square-free
                neg_q_ok = not _is_square_free(n)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The nilradical of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1