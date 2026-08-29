import sympy
from sympy import minpoly, degree, Poly
from sympy.abc import x
from sympy.ntheory import totient
import math
import itertools
import functools

# Top-level setup
# (No specific bindings needed for this domain; variables can be constructed directly)

def conditions(witness):
    try:
        # Since K is unbound in the remaining hypotheses, the witness must provide both n and K.
        if isinstance(witness, tuple) and len(witness) == 2:
            n, K = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        h1_ok = bool(isinstance(n, (int, sympy.Integer)) and n > 0)
    except Exception:
        h1_ok = False

    # ¬Q: The Dirichlet density of the set of prime numbers that split completely in K is NOT equal to 1/\phi(n)
    try:
        # Determine the degree of the Galois closure of K.
        # We assume K is given as a Galois extension (so [L:Q] = deg(K)), 
        # or K is given directly as the integer degree of the Galois closure.
        if isinstance(K, (int, sympy.Integer)):
            deg = int(K)
        elif hasattr(K, 'is_Poly') and K.is_Poly:
            deg = int(K.degree())
        elif hasattr(K, 'free_symbols'):
            p = minpoly(K, x)
            deg = int(degree(p, x))
        elif hasattr(K, 'degree') and callable(K.degree):
            deg = int(K.degree())
        else:
            deg = int(K)
            
        # The density of completely splitting primes is 1/deg.
        # The conclusion states density == 1/totient(n).
        # So the negated conclusion is density != 1/totient(n), which is equivalent to deg != totient(n).
        neg_q_ok = bool(deg != totient(n))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The Dirichlet density of primes splitting completely in K is not equal to 1/\\phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1