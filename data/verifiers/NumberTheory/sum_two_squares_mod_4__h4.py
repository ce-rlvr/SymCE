import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            x = witness.get('x')
            y = witness.get('y')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n, x, y = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: n is an integer
    try:
        h1 = (int(n) == n)
    except Exception:
        h1 = False

    # H2: n \equiv 3 \pmod 4
    try:
        h2 = h1 and (int(n) % 4 == 3)
    except Exception:
        h2 = False

    # H3: x is an integer
    try:
        h3 = (int(x) == x)
    except Exception:
        h3 = False

    # neg_Q: x^2 + y^2 == n
    try:
        lhs = x**2 + y**2
        if isinstance(lhs, sympy.Basic) or isinstance(n, sympy.Basic):
            diff = sympy.simplify(lhs - n)
            neg_q = (diff == 0)
        elif isinstance(lhs, complex) or isinstance(n, complex):
            lhs_c = complex(lhs)
            n_c = complex(n)
            neg_q = math.isclose(lhs_c.real, n_c.real, rel_tol=1e-9, abs_tol=1e-9) and \
                    math.isclose(lhs_c.imag, n_c.imag, rel_tol=1e-9, abs_tol=1e-9)
        elif isinstance(lhs, float) or isinstance(n, float):
            neg_q = math.isclose(float(lhs), float(n), rel_tol=1e-9, abs_tol=1e-9)
        else:
            neg_q = (lhs == n)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n = 3 (mod 4)",
    "H_3: x is an integer",
    "¬Q: x^2 + y^2 == n"
]

N_HYP = 3
NEG_Q_INDEX = 3