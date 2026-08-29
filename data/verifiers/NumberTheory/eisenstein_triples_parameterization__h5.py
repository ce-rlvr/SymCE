import math

# Top-level setup
# (No specific named objects required for this Number Theory conjecture)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 4 + [False]
        x, y, z = witness
    except Exception:
        return [False] * 4 + [False]

    # H_1: x, y, and z are positive integers
    try:
        x_int = int(x)
        y_int = int(y)
        z_int = int(z)
        h1 = (x == x_int) and (y == y_int) and (z == z_int) and (x_int > 0) and (y_int > 0) and (z_int > 0)
        x, y, z = x_int, y_int, z_int
    except Exception:
        h1 = False

    # H_2: gcd(x, y, z) == 1
    try:
        h2 = math.gcd(math.gcd(x, y), z) == 1
    except Exception:
        h2 = False

    # H_3: x^2 + xy + y^2 == z^2
    try:
        h3 = (x**2 + x*y + y**2) == z**2
    except Exception:
        h3 = False

    # H_4: x is odd
    try:
        h4 = (x % 2 == 1)
    except Exception:
        h4 = False

    # neg_Q: The conclusion fails
    try:
        if not h1:
            neg_q = False
        else:
            q_holds = False
            # If x = m^2 - n^2 and y = 2mn + n^2 and z^2 = x^2 + xy + y^2,
            # then n^2 is uniquely determined as (2z - 2x - y) / 3.
            num = 2*z - 2*x - y
            if num > 0 and num % 3 == 0:
                N = num // 3
                n = math.isqrt(N)
                if n * n == N and n > 0:
                    M = x + N
                    m = math.isqrt(M)
                    if m * m == M and m > n:
                        if math.gcd(m, n) == 1 and (m % 3) != (n % 3):
                            if x == m**2 - n**2 and y == 2*m*n + n**2 and z == m**2 + m*n + n**2:
                                q_holds = True
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, and z are positive integers",
    "H_2: gcd(x, y, z) == 1",
    "H_3: x^2 + xy + y^2 == z^2",
    "H_4: x is odd",
    "¬Q: There do not exist coprime positive integers m and n with m > n and m != n mod 3 such that x = m^2 - n^2, y = 2mn + n^2, and z = m^2 + mn + n^2"
]

N_HYP = 4
NEG_Q_INDEX = 4