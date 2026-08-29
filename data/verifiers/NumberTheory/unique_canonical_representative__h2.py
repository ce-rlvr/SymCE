import math
import sympy

# Top-level setup
Z = sympy.S.Integers

def check_is_integer(x):
    if isinstance(x, int):
        return True
    if hasattr(x, 'is_integer'):
        attr = x.is_integer
        if callable(attr):
            try:
                return bool(attr())
            except Exception:
                pass
        elif attr is not None:
            return bool(attr)
    try:
        return float(x).is_integer()
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            a, m = witness
        elif isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: a is an integer
    h1 = check_is_integer(a)

    # neg_Q: not (There exists exactly one integer r such that 0 <= r < m and a == r (mod m))
    try:
        try:
            is_le_zero = bool(m <= 0)
        except Exception:
            is_le_zero = False

        if is_le_zero:
            q = False
        else:
            m_is_int = check_is_integer(m)
            if m_is_int:
                # By the Division Algorithm, if m is a positive integer, 
                # there is exactly one such r iff a is an integer.
                a_is_int = check_is_integer(a)
                q = a_is_int
            else:
                count = 0
                upper = int(math.ceil(float(m)))
                if upper > 100000:
                    q = False
                else:
                    for r in range(0, upper):
                        if r >= m:
                            continue
                        try:
                            k = (a - r) / m
                            if check_is_integer(k):
                                count += 1
                        except Exception:
                            pass
                    q = (count == 1)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: It is not the case that there exists exactly one integer r such that 0 <= r < m and a == r (mod m)"
]

N_HYP = 1
NEG_Q_INDEX = 1