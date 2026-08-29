import sympy
import math
import itertools
import functools

# Top-level setup
n = sympy.Symbol('n')
x = sympy.Symbol('x')
k = sympy.Symbol('k')

def conditions(witness):
    try:
        # Pre-process witness to create a fast callable
        if hasattr(witness, 'free_symbols'):
            symbols = list(witness.free_symbols)
            if len(symbols) == 1:
                sym = symbols[0]
                try:
                    fast_f = sympy.lambdify(sym, witness, modules=['math', 'sympy'])
                    # Test evaluation
                    _ = float(fast_f(1))
                    witness_func = lambda i: float(fast_f(i))
                except Exception:
                    def slow_f(i):
                        return float(witness.subs(sym, i).evalf())
                    witness_func = slow_f
            elif len(symbols) == 0:
                val = float(witness.evalf())
                witness_func = lambda i: val
            else:
                return [False, False]
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 0:
                return [False, False]
            witness_func = lambda i: float(witness[(i - 1) % len(witness)])
        elif isinstance(witness, (int, float)):
            witness_func = lambda i: float(witness)
        elif callable(witness):
            witness_func = lambda i: float(witness(i))
        else:
            return [False, False]
    except Exception:
        return [False, False]

    def get_max_abs(start, count):
        m = 0.0
        for i in range(start, start + count):
            val = witness_func(i)
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Invalid value in sequence")
            if abs(val) > m:
                m = abs(val)
        return m

    # H1: Boundedness
    # A sequence is bounded if there exists M such that |x_n| <= M.
    # We check if the maximum absolute value stabilizes over exponentially increasing intervals.
    h1_ok = False
    try:
        m1 = get_max_abs(1, 1000)
        m2 = get_max_abs(10000, 1000)
        m3 = get_max_abs(100000, 1000)
        m4 = get_max_abs(1000000, 1000)
        
        # If the maximum absolute value strictly and significantly increases across all intervals,
        # the sequence is unbounded.
        if m4 > m3 + 0.05 and m3 > m2 + 0.05 and m2 > m1 + 0.05:
            h1_ok = False
        else:
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: No integer is a subsequential limit of (x_n)
    # This means the sequence of distances to the nearest integer does NOT have 0 as an accumulation point.
    # We check if the distance to the nearest integer remains bounded away from 0 for large n.
    neg_q_ok = False
    try:
        min_dist = 1.0
        for i in range(1000000, 1005000):
            val = witness_func(i)
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Invalid value in sequence")
            dist = abs(val - round(val))
            if dist < min_dist:
                min_dist = dist
        
        # If the minimum distance to an integer in this large-index window is strictly positive,
        # no integer is a subsequential limit.
        if min_dist > 0.01:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exists a real number M such that |x_n| <= M for all n in N",
    "¬Q: No integer is a subsequential limit of (x_n)"
]

N_HYP = 1
NEG_Q_INDEX = 1