import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import *
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            f = witness['f']
        else:
            x, y, f = witness
    except Exception:
        return [False, False, False]
        
    def apply_f(func, val):
        if isinstance(func, (dict, list, tuple)):
            return func[val]
        return func(val)

    # H_1: R and S are rings
    h1_ok = False
    try:
        # Verify that x, y and their images support basic ring operations
        _ = x + y
        _ = x * y
        _ = x - x
        fx = apply_f(f, x)
        fy = apply_f(f, y)
        _ = fx + fy
        _ = fx * fy
        _ = fx - fx
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: x, y in R are orthogonal idempotents
    h2_ok = False
    try:
        zero_R = x - x
        is_idempotent_x = bool(x * x == x)
        is_idempotent_y = bool(y * y == y)
        is_orthogonal_R = bool((x * y == zero_R) and (y * x == zero_R))
        h2_ok = is_idempotent_x and is_idempotent_y and is_orthogonal_R
    except Exception:
        h2_ok = False

    # ¬Q: f(x) and f(y) are not orthogonal idempotents in S
    neg_q_ok = False
    try:
        fx = apply_f(f, x)
        fy = apply_f(f, y)
        zero_S = fx - fx
        
        is_idempotent_fx = bool(fx * fx == fx)
        is_idempotent_fy = bool(fy * fy == fy)
        is_orthogonal_S = bool((fx * fy == zero_S) and (fy * fx == zero_S))
        
        q_holds = is_idempotent_fx and is_idempotent_fy and is_orthogonal_S
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: x, y in R are orthogonal idempotents",
    "¬Q: f(x) and f(y) are not orthogonal idempotents in S"
]

N_HYP = 2
NEG_Q_INDEX = 2