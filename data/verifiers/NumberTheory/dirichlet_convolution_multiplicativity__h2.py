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
# (No named bindings needed for Number Theory; use integers directly)

def get_val(func, n):
    if callable(func):
        return func(n)
    elif isinstance(func, dict):
        return func[n]
    elif isinstance(func, (list, tuple)):
        return func[n - 1]
    else:
        try:
            return func[n]
        except Exception:
            return func[n - 1]

def check_neq(x, y):
    try:
        if hasattr(x, 'free_symbols') or hasattr(y, 'free_symbols'):
            return bool(sympy.simplify(x - y) != 0)
        return x != y
    except Exception:
        return x != y

def is_multiplicative(func, max_n=100):
    try:
        try:
            if check_neq(get_val(func, 1), 1):
                return False
        except (IndexError, KeyError):
            return False
            
        for a in range(1, max_n + 1):
            for b in range(1, max_n // a + 1):
                if math.gcd(a, b) == 1:
                    try:
                        val_ab = get_val(func, a * b)
                        val_a = get_val(func, a)
                        val_b = get_val(func, b)
                        if check_neq(val_ab, val_a * val_b):
                            return False
                    except (IndexError, KeyError):
                        continue
        return True
    except Exception:
        return False

def conv_val(f, g, n):
    res = 0
    for d in range(1, n + 1):
        if n % d == 0:
            res += get_val(f, d) * get_val(g, n // d)
    return res

def is_not_multiplicative_conv(f, g, max_n=100):
    try:
        try:
            h1 = conv_val(f, g, 1)
            if check_neq(h1, 1):
                return True
        except (IndexError, KeyError):
            pass
            
        for a in range(1, max_n + 1):
            for b in range(1, max_n // a + 1):
                if math.gcd(a, b) == 1:
                    try:
                        hab = conv_val(f, g, a * b)
                        ha = conv_val(f, g, a)
                        hb = conv_val(f, g, b)
                        if check_neq(hab, ha * hb):
                            return True
                    except (IndexError, KeyError):
                        continue
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        f, g = witness
        
        h1 = is_multiplicative(f, 100)
        neg_q = is_not_multiplicative_conv(f, g, 100)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f is a multiplicative arithmetic function",
    "¬Q: The Dirichlet convolution f * g is not a multiplicative arithmetic function"
]

N_HYP = 1
NEG_Q_INDEX = 1