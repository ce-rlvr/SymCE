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
# No named bindings needed for Number Theory; use integers directly.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness['n']
            k = witness['k']
        else:
            n, k = witness
            
        n_sym = sympy.sympify(n)
        k_sym = sympy.sympify(k)
        
        if not n_sym.is_integer or not k_sym.is_integer:
            return [False, False]
            
        n = int(n_sym)
        k = int(k_sym)
    except Exception:
        return [False, False]

    # H_1: k is a positive integer
    try:
        h1_ok = bool(k > 0)
    except Exception:
        h1_ok = False

    # ¬Q: phi(n^k) != n^{k-1} phi(n)
    try:
        lhs = sympy.ntheory.totient(n**k)
        rhs = (n**(k-1)) * sympy.ntheory.totient(n)
        neg_q_ok = bool(lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: phi(n^k) != n^{k-1} phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1