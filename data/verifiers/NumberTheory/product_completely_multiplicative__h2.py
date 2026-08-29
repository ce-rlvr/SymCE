import sympy
import math
import itertools
import functools

# No specific named bindings needed for Number Theory

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "If f is a completely multiplicative arithmetic function and h(n) = f(n)g(n), 
    then h is completely multiplicative."
    
    The witness should be a tuple (f, g) or an object with attributes f and g,
    where f and g are arithmetic functions (callables or subscriptables).
    """
    try:
        if hasattr(witness, 'f') and hasattr(witness, 'g'):
            f = witness.f
            g = witness.g
        else:
            f, g = witness
    except Exception:
        return [False, False, False]

    def eval_f(n):
        if callable(f): 
            return f(n)
        return f[n]

    def eval_g(n):
        if callable(g): 
            return g(n)
        return g[n]

    LIMIT = 256

    # H_1: f is a completely multiplicative arithmetic function
    try:
        h1 = True
        if eval_f(1) != 1:
            h1 = False
        else:
            for a in range(1, LIMIT + 1):
                for b in range(1, LIMIT // a + 1):
                    if eval_f(a * b) != eval_f(a) * eval_f(b):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: h is an arithmetic function defined by h(n) = f(n)g(n) for all positive integers n
    try:
        h2 = True
        # Verify that f and g can be evaluated on the domain up to LIMIT
        for n in range(1, LIMIT + 1):
            _ = eval_f(n)
            _ = eval_g(n)
    except Exception:
        h2 = False

    # neg_Q: The function h is not completely multiplicative
    try:
        def eval_h(n):
            return eval_f(n) * eval_g(n)
            
        is_h_mult = True
        if eval_h(1) != 1:
            is_h_mult = False
        else:
            for a in range(1, LIMIT + 1):
                for b in range(1, LIMIT // a + 1):
                    if eval_h(a * b) != eval_h(a) * eval_h(b):
                        is_h_mult = False
                        break
                if not is_h_mult:
                    break
        neg_q = not is_h_mult
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a completely multiplicative arithmetic function",
    "H_2: h is an arithmetic function defined by h(n) = f(n)g(n) for all positive integers n",
    "¬Q: The function h is not completely multiplicative"
]

N_HYP = 2
NEG_Q_INDEX = 2