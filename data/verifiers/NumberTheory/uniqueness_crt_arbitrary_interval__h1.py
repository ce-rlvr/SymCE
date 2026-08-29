import math
import functools
import sympy

def _lcm(x, y):
    if x == 0 or y == 0:
        return 0
    return abs(x * y) // math.gcd(int(x), int(y))

def _prod(iterable):
    return functools.reduce(lambda x, y: x * y, iterable, 1)

def is_int(x):
    return isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Chinese Remainder Theorem 
    uniqueness conjecture.
    
    The witness should be a dictionary with keys:
      'm': list of moduli (m_1, ..., m_k)
      'a': list of remainders (a_1, ..., a_k)
      'M': the product of the moduli
      'c': the start of the interval
    """
    try:
        m = witness['m']
        a = witness['a']
        M = witness['M']
        c = witness['c']
    except Exception:
        return [False, False, False, False]
    
    # H_1: M = m_1 m_2 ... m_k
    try:
        h1 = (isinstance(m, (list, tuple)) and 
              isinstance(a, (list, tuple)) and 
              len(m) == len(a) and 
              all(is_int(x) for x in m) and 
              is_int(M) and 
              M == _prod(m))
    except Exception:
        h1 = False

    # H_2: a_1, a_2, ..., a_k are integers
    try:
        h2 = isinstance(a, (list, tuple)) and all(is_int(x) for x in a)
    except Exception:
        h2 = False

    # H_3: c is an integer
    try:
        h3 = is_int(c)
    except Exception:
        h3 = False

    # ¬Q: The number of solutions x in [c, c + M) is not exactly 1
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            # Check if the system of congruences is solvable
            solvable = True
            for i in range(len(m)):
                for j in range(i + 1, len(m)):
                    g = math.gcd(int(m[i]), int(m[j]))
                    if (a[i] - a[j]) % g != 0:
                        solvable = False
                        break
                if not solvable:
                    break
            
            if solvable:
                if M <= 0:
                    # The interval [c, c + M) is empty
                    count = 0
                else:
                    # If solvable, solutions are unique modulo L = lcm(m_1, ..., m_k)
                    L = functools.reduce(_lcm, m) if len(m) > 0 else 1
                    # Since M = prod(m), M is a multiple of L.
                    # The number of solutions in any interval of length M is exactly M // L.
                    count = M // L
            else:
                count = 0
                
            neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M = m_1 m_2 ... m_k",
    "H_2: a_1, a_2, ..., a_k are integers",
    "H_3: c is an integer",
    "¬Q: The number of solutions x in [c, c + M) is not exactly 1"
]

N_HYP = 3
NEG_Q_INDEX = 3