import sympy
import sympy.ntheory
from sympy.abc import n
import math
import itertools
import functools

# Top-level setup
# (No special groups or matrices needed for this number theory conjecture)

def get_max_n(witness, default=50):
    if isinstance(witness, (list, tuple)):
        return len(witness) - 1
    elif isinstance(witness, dict):
        keys = [k for k in witness.keys() if isinstance(k, int) and k >= 1]
        return max(keys) if keys else 0
    return default

def eval_f(f, k):
    if callable(f):
        return f(k)
    elif isinstance(f, dict):
        return f[k]
    elif isinstance(f, (list, tuple)):
        return f[k]
    elif isinstance(f, sympy.Expr):
        free_syms = list(f.free_symbols)
        if len(free_syms) == 1:
            return f.subs(free_syms[0], k)
        elif len(free_syms) == 0:
            return f
        else:
            return f.subs(sympy.Symbol('n'), k)
    else:
        raise TypeError("Witness must be callable, dict, list, or sympy Expr")

def conditions(witness) -> list[bool]:
    max_n = get_max_n(witness, 50)
    if max_n < 1:
        return [False, False]
    max_n = min(max_n, 100)

    # H_1: f is an arithmetic function
    h1 = False
    try:
        for i in range(1, max_n + 1):
            val = eval_f(witness, i)
            if not isinstance(val, (int, float, complex)):
                sympy.sympify(val)
        h1 = True
    except Exception:
        h1 = False

    # neg_Q: The Dirichlet inverse of f is NOT \mu(n)f(n)
    neg_q = False
    try:
        for i in range(1, max_n + 1):
            conv = 0
            for d in sympy.ntheory.divisors(i):
                term1 = eval_f(witness, d)
                term2 = sympy.ntheory.mobius(i // d) * eval_f(witness, i // d)
                conv += term1 * term2
            
            expected = 1 if i == 1 else 0
            diff = sympy.simplify(conv - expected)
            
            if isinstance(diff, (int, float, complex)):
                if abs(diff) > 1e-9:
                    neg_q = True
                    break
            else:
                if diff.is_number:
                    if abs(complex(diff)) > 1e-9:
                        neg_q = True
                        break
                elif diff != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is an arithmetic function",
    "¬Q: The Dirichlet inverse of f is not \mu(n)f(n) for all positive integers n"
]

N_HYP = 1
NEG_Q_INDEX = 1