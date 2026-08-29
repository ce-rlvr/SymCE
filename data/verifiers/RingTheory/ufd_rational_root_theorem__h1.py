import math

def is_valid_element(e):
    return (isinstance(e, tuple) and len(e) == 2 and 
            type(e[0]) is int and type(e[1]) is int)

def is_square_free(n):
    if type(n) is not int or n == 0: 
        return False
    n = abs(n)
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % (i * i) == 0:
            return False
    return True

def add(A, B):
    return (A[0] + B[0], A[1] + B[1])

def mul(A, B, d):
    return (A[0]*B[0] + d*A[1]*B[1], A[0]*B[1] + A[1]*B[0])

def norm(A, d):
    return A[0]**2 - d * A[1]**2

def divides(A, B, d):
    nA = norm(A, d)
    if nA == 0:
        return B[0] == 0 and B[1] == 0
    conjA = (A[0], -A[1])
    num = mul(B, conjA, d)
    return num[0] % nA == 0 and num[1] % nA == 0

def is_coprime(p, q, d):
    if d >= 0:
        return False
    np = norm(p, d)
    nq = norm(q, d)
    if np == 0 and nq == 0:
        return False
    g = math.gcd(np, nq)
    abs_d = -d
    max_c2 = int(math.isqrt(g // abs_d))
    for c2 in range(-max_c2 - 1, max_c2 + 2):
        rem = g - abs_d * c2**2
        if rem < 0:
            continue
        max_c1 = int(math.isqrt(rem))
        for c1 in range(-max_c1 - 1, max_c1 + 2):
            C = (c1, c2)
            nC = norm(C, d)
            if nC > 1 and g % nC == 0:
                if divides(C, p, d) and divides(C, q, d):
                    return False
    return True

def power(A, k, d):
    res = (1, 0)
    base = A
    while k > 0:
        if k % 2 == 1:
            res = mul(res, base, d)
        base = mul(base, base, d)
        k //= 2
    return res

def eval_poly_homog(coeffs, p, q, d):
    n = len(coeffs) - 1
    total = (0, 0)
    for i, a in enumerate(coeffs):
        p_pow = power(p, i, d)
        q_pow = power(q, n - i, d)
        term = mul(a, mul(p_pow, q_pow, d), d)
        total = add(total, term)
    return total == (0, 0)

def conditions(witness):
    try:
        d, coeffs, p, q = witness
    except Exception:
        return [False] * 5

    try:
        h1 = type(d) is int and d < 0 and is_square_free(d)
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(coeffs, list) and len(coeffs) >= 2 and 
              all(is_valid_element(c) for c in coeffs) and 
              coeffs[-1] != (0, 0))
    except Exception:
        h2 = False

    try:
        h3 = is_valid_element(p) and is_valid_element(q) and q != (0, 0) and is_coprime(p, q, d)
    except Exception:
        h3 = False

    try:
        h4 = eval_poly_homog(coeffs, p, q, d)
    except Exception:
        h4 = False

    try:
        a_n = coeffs[-1]
        a_0 = coeffs[0]
        q_div_an = divides(q, a_n, d)
        p_div_a0 = divides(p, a_0, d)
        neg_q = not (q_div_an and p_div_a0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is the fraction field of R",
    "H_2: f(x) is a polynomial over R of degree n >= 1",
    "H_3: p and q are coprime elements of R",
    "H_4: The element p/q in K is a root of f(x)",
    "¬Q: q does not divide a_n or p does not divide a_0 in R"
]

N_HYP = 4
NEG_Q_INDEX = 4