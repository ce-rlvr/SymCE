import sympy
from sympy.ntheory import factorint

# Top-level setup
# Witness format:
# The witness should be a tuple (n, M_list) or a dictionary {'n': n, 'M_list': M_list}.
# - n is an integer >= 2 representing the commutative local ring R = Z/nZ.
# - M_list is a list of positive integers [m_1, m_2, ..., m_k] representing 
#   the finitely generated R-module M = Z/m_1 Z \oplus Z/m_2 Z \oplus ... \oplus Z/m_k Z.
# Example: witness = (4, [2])  # R = Z/4Z, M = Z/2Z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            M_list = witness.get('M_list', [])
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, M_list = witness
        else:
            return [False, False, False]
            
        n = int(n)
        M_list = [int(m) for m in M_list]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative local ring with maximal ideal \mathfrak{m}
    # For R = Z/nZ, it is local iff n is a prime power p^k (k >= 1).
    try:
        if n < 2:
            h1 = False
        else:
            factors = factorint(n)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H_2: M is a finitely generated R-module
    # M is a finite direct sum of cyclic groups Z/m_i Z.
    # It is an R-module iff it is annihilated by n, meaning each m_i divides n.
    try:
        h2 = all(m > 0 and n % m == 0 for m in M_list)
    except Exception:
        h2 = False

    # ¬Q: M is not a free R-module
    # M is free over Z/nZ iff it is isomorphic to (Z/nZ)^d for some d >= 0.
    # This means all non-trivial cyclic components must be isomorphic to Z/nZ.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            is_free = all(m == 1 or m == n for m in M_list)
            neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring with maximal ideal m",
    "H_2: M is a finitely generated R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2