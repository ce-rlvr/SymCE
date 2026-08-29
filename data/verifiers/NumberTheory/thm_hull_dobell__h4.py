import math
import sympy
from sympy.ntheory import factorint

def is_integer(x):
    if isinstance(x, bool):
        return False
    return isinstance(x, int) or isinstance(x, sympy.Integer)

def conditions(witness):
    try:
        m, a, c = witness
    except Exception:
        return [False] * 5
        
    try:
        h1 = is_integer(m) and m > 1
    except Exception:
        h1 = False
        
    try:
        h2 = is_integer(a) and is_integer(c) and a > 0
    except Exception:
        h2 = False
        
    try:
        h3 = math.gcd(int(c), int(m)) == 1
    except Exception:
        h3 = False
        
    try:
        h4 = (int(m) % 4 != 0) or ((int(a) - 1) % 4 == 0)
    except Exception:
        h4 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            m_int = int(m)
            a_int = int(a)
            c_int = int(c)
            if m_int > 10**6:
                is_full_period = True
                if math.gcd(c_int, m_int) != 1:
                    is_full_period = False
                elif m_int % 4 == 0 and (a_int - 1) % 4 != 0:
                    is_full_period = False
                else:
                    for p in factorint(m_int):
                        if (a_int - 1) % p != 0:
                            is_full_period = False
                            break
                neg_q = not is_full_period
            else:
                visited = set()
                x = 0
                for _ in range(m_int):
                    if x in visited:
                        break
                    visited.add(x)
                    x = (a_int * x + c_int) % m_int
                neg_q = len(visited) != m_int
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer greater than 1",
    "H_2: a and c are integers with a > 0",
    "H_3: gcd(c, m) = 1",
    "H_4: If m is divisible by 4, then a - 1 is also divisible by 4",
    "¬Q: The sequence does not have a period of exactly m for some initial value x_0"
]

N_HYP = 4
NEG_Q_INDEX = 4