import math
import itertools
import sympy
from sympy.ntheory import factorint
from sympy.polys.galoistools import gf_mul, gf_rem, gf_sub, gf_add, gf_irreducible
from sympy.polys.domains import ZZ

def is_prime_power(q):
    try:
        if not isinstance(q, (int, sympy.Integer)) or q < 2:
            return False
        f = factorint(int(q))
        return len(f) == 1
    except Exception:
        return False

def poly_strip(f):
    i = 0
    while i < len(f) and f[i] == 0:
        i += 1
    return f[i:]

def dickson_poly_eval_fast(n, x_val, a_val, q):
    if n == 0:
        return 2 % q
    elif n == 1:
        return x_val % q
    
    def mat_mult(A, B):
        return [
            [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % q, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % q],
            [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % q, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % q]
        ]
        
    def mat_pow(A, p_pow):
        res = [[1, 0], [0, 1]]
        base = A
        while p_pow > 0:
            if p_pow % 2 == 1:
                res = mat_mult(res, base)
            base = mat_mult(base, base)
            p_pow //= 2
        return res

    M = [[x_val % q, (-a_val) % q], [1, 0]]
    M_pow = mat_pow(M, n - 1)
    
    D_n = (M_pow[0][0] * x_val + M_pow[0][1] * 2) % q
    return D_n

def dickson_poly_eval_gf_fast(n, x_val, a_val, P, p):
    if n == 0:
        return poly_strip([2 % p])
    elif n == 1:
        return poly_strip(x_val)
        
    def gf_mult_poly(A, B):
        return gf_rem(gf_mul(A, B, p, ZZ), P, p, ZZ)
        
    def mat_mult(A, B):
        C00 = gf_add(gf_mult_poly(A[0][0], B[0][0]), gf_mult_poly(A[0][1], B[1][0]), p, ZZ)
        C01 = gf_add(gf_mult_poly(A[0][0], B[0][1]), gf_mult_poly(A[0][1], B[1][1]), p, ZZ)
        C10 = gf_add(gf_mult_poly(A[1][0], B[0][0]), gf_mult_poly(A[1][1], B[1][0]), p, ZZ)
        C11 = gf_add(gf_mult_poly(A[1][0], B[0][1]), gf_mult_poly(A[1][1], B[1][1]), p, ZZ)
        return [[C00, C01], [C10, C11]]
        
    def mat_pow(A, power):
        res = [[[1], []], [[], [1]]]
        base = A
        while power > 0:
            if power % 2 == 1:
                res = mat_mult(res, base)
            base = mat_mult(base, base)
            power //= 2
        return res

    minus_a = gf_sub([], a_val, p, ZZ)
    M = [[x_val, minus_a], [[1], []]]
    M_pow = mat_pow(M, n - 1)
    
    term1 = gf_mult_poly(M_pow[0][0], x_val)
    term2 = gf_mult_poly(M_pow[0][1], [2 % p])
    D_n = gf_add(term1, term2, p, ZZ)
    
    return poly_strip(D_n)

def is_permutation_gf(n, a_val, p, k):
    P = gf_irreducible(k, p, ZZ)
    
    if isinstance(a_val, (int, sympy.Integer)):
        a_val = [int(a_val) % p]
    elif isinstance(a_val, (list, tuple)):
        a_val = [int(c) for c in a_val]
    else:
        raise ValueError("Invalid a_val")
        
    a_val = poly_strip(a_val)
    
    elements = list(itertools.product(range(p), repeat=k))
    seen = set()
    for x_tup in elements:
        x_val = poly_strip(list(x_tup))
        val = dickson_poly_eval_gf_fast(n, x_val, a_val, P, p)
        val_tup = tuple(val)
        if val_tup in seen:
            return False
        seen.add(val_tup)
    return True

def is_permutation(n, a, q):
    if q > 10000:
        raise ValueError("q too large")
    
    f = factorint(int(q))
    p = list(f.keys())[0]
    k = f[p]
    
    n = int(n)
    
    if k == 1:
        a = int(a)
        seen = set()
        for x in range(q):
            val = dickson_poly_eval_fast(n, x, a, q)
            if val in seen:
                return False
            seen.add(val)
        return True
    else:
        return is_permutation_gf(n, a, p, k)

def conditions(witness):
    try:
        q, n, a = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: q is a prime power
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    # H2: n is a positive integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h2 = False
        
    # H3: a is in F_q
    try:
        if h1:
            f = factorint(int(q))
            p = list(f.keys())[0]
            k = f[p]
            if k == 1:
                h3 = isinstance(a, (int, sympy.Integer)) and 0 <= a < q
            else:
                if isinstance(a, (int, sympy.Integer)):
                    h3 = 0 <= a < p
                elif isinstance(a, (list, tuple)):
                    h3 = all(isinstance(c, (int, sympy.Integer)) and 0 <= c < p for c in a) and len(a) <= k
                else:
                    h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: D_n(x, a) induces a permutation iff gcd(n, q^2 - 1) == 1
    try:
        if h1 and h2 and h3:
            is_perm = is_permutation(n, a, q)
            gcd_cond = (math.gcd(int(n), int(q**2 - 1)) == 1)
            neg_q = not (is_perm == gcd_cond)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: n is a positive integer",
    "H_3: D_n(x, a) is the n-th Dickson polynomial of the first kind over F",
    "¬Q: D_n(x, a) induces a permutation on F if and only if gcd(n, q^2 - 1) = 1 is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3