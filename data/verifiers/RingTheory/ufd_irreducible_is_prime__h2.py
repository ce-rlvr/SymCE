import sympy
from sympy import Poly
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
Z = sympy.S.Integers
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If R is a UFD, then any element p in R is a prime element."
    """
    # The witness can be just the element p, or a tuple (R, p).
    p = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        _, p = witness

    h1_ok = False
    p_eval = None

    try:
        # H_1: R is a unique factorization domain
        # We support the ring of integers Z and polynomial rings over Z or Q, which are UFDs.
        if isinstance(p, Poly):
            h1_ok = p.domain in (sympy.ZZ, sympy.QQ)
            p_eval = p
        elif isinstance(p, sympy.Expr) and p.free_symbols:
            poly_p = Poly(p)
            h1_ok = poly_p.domain in (sympy.ZZ, sympy.QQ)
            p_eval = poly_p
        else:
            h1_ok = isinstance(p, (int, sympy.Integer))
            p_eval = p
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        # ¬Q: p is not a prime element in R
        if h1_ok:
            if isinstance(p_eval, Poly):
                # In a UFD, prime elements are irreducible elements.
                neg_q_ok = not p_eval.is_irreducible
            else:
                # In Z, an element is prime iff its absolute value is a prime number.
                # 0 and units (1, -1) are not prime elements, which isprime handles correctly (returns False).
                val = abs(int(p_eval))
                neg_q_ok = not sympy.isprime(val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1