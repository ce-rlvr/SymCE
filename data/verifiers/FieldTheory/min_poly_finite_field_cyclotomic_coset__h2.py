import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def mod_q(x, q):
    if isinstance(x, sp.Matrix):
        return x.applyfunc(lambda e: e % q)
    elif isinstance(x, (int, sp.Integer)):
        return x % q
    else:
        raise ValueError(f"Unsupported type: {type(x)}")

def is_zero(x, q):
    x_mod = mod_q(x, q)
    if isinstance(x_mod, sp.Matrix):
        return x_mod.is_zero_matrix
    else:
        return x_mod == 0

def eq(x, y, q):
    return is_zero(x - y, q)

def get_zero(x):
    if isinstance(x, sp.Matrix):
        return sp.zeros(x.shape[0], x.shape[1])
    else:
        return 0

def get_one(x):
    if isinstance(x, sp.Matrix):
        return sp.eye(x.shape[0])
    else:
        return 1

def power(x, k, q):
    if k == 0:
        return get_one(x)
    res = get_one(x)
    base = mod_q(x, q)
    while k > 0:
        if k % 2 == 1:
            res = mod_q(res * base, q)
        base = mod_q(base * base, q)
        k //= 2
    return res

def get_scalar(x, q):
    x_mod = mod_q(x, q)
    if isinstance(x_mod, sp.Matrix):
        if x_mod.shape[0] != x_mod.shape[1]:
            return None
        n = x_mod.shape[0]
        if n == 0:
            return 0
        c = x_mod[0, 0]
        expected = mod_q(c * sp.eye(n), q)
        if x_mod == expected:
            return c
        else:
            return None
    else:
        return x_mod

def check_H1(q):
    if not isinstance(q, (int, sp.Integer)):
        return False
    # We require q to be prime so that Z/qZ is a field F_q.
    return sp.isprime(q)

def check_H2(q, alpha, d):
    if not isinstance(d, (int, sp.Integer)) or d < 1:
        return False
    for k in range(1, d + 1):
        val = power(alpha, q**k, q)
        if eq(val, alpha, q):
            if k == d:
                return True
            else:
                return False
    return False

def poly_mul(A, B, q):
    degA = len(A) - 1
    degB = len(B) - 1
    zero = get_zero(A[0])
    res = [zero] * (degA + degB + 1)
    for i in range(degA + 1):
        for j in range(degB + 1):
            term = mod_q(A[i] * B[j], q)
            res[i+j] = mod_q(res[i+j] + term, q)
    return res

def get_product(q, alpha, d):
    one = get_one(alpha)
    P = [one]
    for i in range(d):
        root = power(alpha, q**i, q)
        factor = [mod_q(-root, q), one]
        P = poly_mul(P, factor, q)
    return P

def rank_mod_p(vectors, p):
    if not vectors:
        return 0
    mat = [list(row) for row in vectors]
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    for c in range(cols):
        pivot = -1
        for r in range(rank, rows):
            if mat[r][c] % p != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][c] % p, p - 2, p)
        for r in range(rank + 1, rows):
            factor = (mat[r][c] * inv) % p
            for k in range(c, cols):
                mat[r][k] = (mat[r][k] - factor * mat[rank][k]) % p
        rank += 1
    return rank

def check_Q(q, alpha, d):
    P = get_product(q, alpha, d)
    scalar_coeffs = []
    for c in P:
        s = get_scalar(c, q)
        if s is None:
            return False
        scalar_coeffs.append(s)
    
    val = get_zero(alpha)
    curr = get_one(alpha)
    for s in scalar_coeffs:
        term = mod_q(s * curr, q)
        val = mod_q(val + term, q)
        curr = mod_q(curr * alpha, q)
    if not is_zero(val, q):
        return False
        
    vectors = []
    curr = get_one(alpha)
    for i in range(d):
        if isinstance(curr, sp.Matrix):
            vectors.append(list(curr))
        else:
            vectors.append([curr])
        curr = mod_q(curr * alpha, q)
        
    r = rank_mod_p(vectors, q)
    if r < d:
        return False
        
    return True

def conditions(witness):
    try:
        q, alpha, d = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_H1(q)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(q, alpha, d)
    except Exception:
        h2 = False
        
    try:
        q_holds = check_Q(q, alpha, d)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: d is the smallest positive integer such that alpha^(q^d) = alpha",
    "not Q: The minimal polynomial of alpha over F_q is NOT given by the product"
]

N_HYP = 2
NEG_Q_INDEX = 2