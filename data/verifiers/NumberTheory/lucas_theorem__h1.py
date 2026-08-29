import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = witness['m']
            n = witness['n']
            p = witness['p']
        else:
            m, n, p = witness[:3]
    except Exception:
        return [False, False, False, False]

    # H_1: m and n are non-negative integers
    try:
        h1 = isinstance(m, int) and isinstance(n, int) and m >= 0 and n >= 0
    except Exception:
        h1 = False

    # H_2: m = m_k p^k + ... is the base p expansion of m
    # This implies p is a valid base (integer >= 2)
    try:
        h2 = isinstance(p, int) and p >= 2 and isinstance(m, int) and m >= 0
    except Exception:
        h2 = False

    # H_3: n = n_k p^k + ... is the base p expansion of n
    try:
        h3 = isinstance(p, int) and p >= 2 and isinstance(n, int) and n >= 0
    except Exception:
        h3 = False

    # neg_Q: \binom{m}{n} \not\equiv \prod \binom{m_i}{n_i} \pmod p
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            def base_p(x, base):
                if x == 0:
                    return [0]
                digits = []
                while x > 0:
                    digits.append(x % base)
                    x //= base
                return digits
            
            m_digits = base_p(m, p)
            n_digits = base_p(n, p)
            max_len = max(len(m_digits), len(n_digits))
            m_digits += [0] * (max_len - len(m_digits))
            n_digits += [0] * (max_len - len(n_digits))
            
            prod = 1
            for mi, ni in zip(m_digits, n_digits):
                prod = (prod * math.comb(mi, ni)) % p
                
            lhs = math.comb(m, n) % p
            neg_q = (lhs != prod)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are non-negative integers",
    "H_2: m = m_k p^k + \\dots + m_1 p + m_0 is the base p expansion of m",
    "H_3: n = n_k p^k + \\dots + n_1 p + n_0 is the base p expansion of n",
    "¬Q: \\binom{m}{n} \\not\\equiv \\prod_{i=0}^k \\binom{m_i}{n_i} \\pmod p"
]

N_HYP = 3
NEG_Q_INDEX = 3