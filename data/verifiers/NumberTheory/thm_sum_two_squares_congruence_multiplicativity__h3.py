import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        c, m, n = witness
    except Exception:
        return [False, False, False]
    
    def is_integer_val(x):
        if isinstance(x, int) and not isinstance(x, bool):
            return True
        if hasattr(x, 'is_integer'):
            if callable(x.is_integer):
                return x.is_integer()
            else:
                return bool(x.is_integer)
        return False

    try:
        h1 = bool(is_integer_val(c))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_integer_val(m) and is_integer_val(n) and m > 0 and n > 0)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            c_int = int(c)
            m_int = int(m)
            n_int = int(n)
            
            def count_solutions(val, k):
                if k <= 0:
                    return 0
                freq = {}
                for x in range(k):
                    sq = (x * x) % k
                    freq[sq] = freq.get(sq, 0) + 1
                ans = 0
                for sq1, f1 in freq.items():
                    sq2 = (val - sq1) % k
                    if sq2 in freq:
                        ans += f1 * freq[sq2]
                return ans
            
            sol_mn = count_solutions(c_int, m_int * n_int)
            sol_m = count_solutions(c_int, m_int)
            sol_n = count_solutions(c_int, n_int)
            
            neg_q = bool(sol_mn != sol_m * sol_n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: c is an integer",
    "H_2: m and n are positive integers",
    "¬Q: The number of solutions mod mn is NOT equal to the product of the number of solutions mod m and mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2