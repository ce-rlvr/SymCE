import math

CONDITION_LABELS = [
    "H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers",
    "H_2: a_1, a_2, ..., a_k are integers",
    "¬Q: The system of congruences does not have a unique solution modulo the product m_1 m_2 ... m_k"
]

N_HYP = 2
NEG_Q_INDEX = 2

def _lcm(x, y):
    if x == 0 and y == 0:
        return 0
    return abs(x * y) // math.gcd(x, y)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m = witness['m']
            a = witness['a']
        elif hasattr(witness, 'm') and hasattr(witness, 'a'):
            m = witness.m
            a = witness.a
        elif len(witness) == 2 and isinstance(witness[0], (list, tuple)) and isinstance(witness[1], (list, tuple)):
            m = witness[0]
            a = witness[1]
        else:
            m = [x[0] for x in witness]
            a = [x[1] for x in witness]
    except Exception:
        return [False, False, False]

    if len(m) != len(a):
        return [False, False, False]

    # H1: m_i are pairwise coprime positive integers
    try:
        h1 = True
        for x in m:
            if not isinstance(x, int) or x <= 0:
                h1 = False
                break
        if h1:
            for i in range(len(m)):
                for j in range(i + 1, len(m)):
                    if math.gcd(m[i], m[j]) != 1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: a_i are integers
    try:
        h2 = all(isinstance(x, int) for x in a)
    except Exception:
        h2 = False

    # neg_Q: The system does NOT have a unique solution modulo the product
    try:
        solution_exists = True
        for i in range(len(m)):
            for j in range(i + 1, len(m)):
                g = math.gcd(m[i], m[j])
                if g == 0:
                    if a[i] != a[j]:
                        solution_exists = False
                        break
                else:
                    if (a[i] - a[j]) % g != 0:
                        solution_exists = False
                        break
            if not solution_exists:
                break
        
        if not solution_exists:
            q = False
        else:
            if len(m) == 0:
                l = 1
                p = 1
            else:
                l = abs(m[0])
                p = m[0]
                for i in range(1, len(m)):
                    l = _lcm(l, m[i])
                    p *= m[i]
            q = (l == abs(p))
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]