import math

def conditions(witness):
    try:
        # Witness should be a tuple or list of three integers: (x, y, z)
        if len(witness) != 3:
            return [False, False, False]
        x, y, z = witness
        x = int(x)
        y = int(y)
        z = int(z)
    except Exception:
        return [False, False, False]

    # H_1: x, y, and z are positive integers satisfying x^2 + y^2 = z^2
    try:
        h1 = (x > 0 and y > 0 and z > 0) and (x**2 + y**2 == z**2)
    except Exception:
        h1 = False

    # H_2: x, y, and z are pairwise coprime
    try:
        h2 = (math.gcd(x, y) == 1) and (math.gcd(y, z) == 1) and (math.gcd(x, z) == 1)
    except Exception:
        h2 = False

    # ¬Q: There do NOT exist coprime positive integers m and n with m > n, exactly one of which is even,
    # such that x = 2mn, y = m^2 - n^2, and z = m^2 + n^2.
    try:
        q_holds = False
        # If such m and n exist, they are uniquely determined by y and z:
        # z + y = 2m^2  =>  m^2 = (z + y) / 2
        # z - y = 2n^2  =>  n^2 = (z - y) / 2
        if (z + y) % 2 == 0 and (z - y) % 2 == 0:
            m_sq = (z + y) // 2
            n_sq = (z - y) // 2
            if m_sq > 0 and n_sq > 0:
                m = math.isqrt(m_sq)
                n = math.isqrt(n_sq)
                if m**2 == m_sq and n**2 == n_sq:
                    if m > n and math.gcd(m, n) == 1 and (m % 2 != n % 2):
                        if x == 2 * m * n and y == m**2 - n**2 and z == m**2 + n**2:
                            q_holds = True
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, and z are positive integers satisfying x^2 + y^2 = z^2",
    "H_2: x, y, and z are pairwise coprime",
    "¬Q: There do not exist coprime positive integers m and n with m > n, exactly one even, such that x = 2mn, y = m^2 - n^2, and z = m^2 + n^2"
]

N_HYP = 2
NEG_Q_INDEX = 2