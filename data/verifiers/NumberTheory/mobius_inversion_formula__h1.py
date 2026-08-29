import sympy
from sympy.ntheory import mobius, divisors
from sympy.abc import n
import math
import itertools
import functools

def is_equal(a, b):
    if a == b:
        return True
    try:
        diff = sympy.expand(a - b)
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        if diff == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the hypothesis but fails the conclusion.
    The witness should be a tuple (f, g) where f and g are either:
      - callables (functions)
      - dictionaries mapping positive integers to values
      - lists/tuples (0-indexed, so f[n] corresponds to n)
      - sympy expressions in terms of sympy.abc.n
    """
    try:
        f, g = witness
    except Exception:
        return [False, False]
        
    if isinstance(f, dict):
        domain = [k for k in f.keys() if isinstance(k, int) and k > 0]
    elif isinstance(f, (list, tuple)):
        domain = list(range(1, len(f)))
    else:
        domain = list(range(1, 101))
        
    if not domain:
        return [False, False]
        
    def eval_f(n_val):
        if isinstance(f, dict): return f[n_val]
        if isinstance(f, (list, tuple)): return f[n_val]
        if hasattr(f, 'subs'): return f.subs(n, n_val)
        return f(n_val)
        
    def eval_g(n_val):
        if isinstance(g, dict): return g[n_val]
        if isinstance(g, (list, tuple)): return g[n_val]
        if hasattr(g, 'subs'): return g.subs(n, n_val)
        return g(n_val)

    try:
        h1 = True
        for k in domain:
            divs = divisors(k)
            s = eval_g(divs[0])
            for d in divs[1:]:
                s = s + eval_g(d)
            if not is_equal(eval_f(k), s):
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        neg_q = False
        for k in domain:
            divs = divisors(k)
            s = mobius(divs[0]) * eval_f(k // divs[0])
            for d in divs[1:]:
                s = s + mobius(d) * eval_f(k // d)
            if not is_equal(eval_g(k), s):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(n) = sum_{d|n} g(d) for all positive integers n",
    "¬Q: g(n) != sum_{d|n} mu(d) f(n/d) for some positive integer n"
]

N_HYP = 1
NEG_Q_INDEX = 1