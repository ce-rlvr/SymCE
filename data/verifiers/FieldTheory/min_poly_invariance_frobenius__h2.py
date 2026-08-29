from sympy import isprime, Matrix, eye, zeros, Symbol, Poly, GF
import itertools
import math
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def solve_mod_p(M, v, p):
    """Solves the linear system M * c = v mod p. Returns the solution vector c or None."""
    m = M.shape[0]
    k = M.shape[1]
    A = Matrix.hstack(M, v).as_mutable()
    
    row = 0
    for col in range(k):
        pivot = -1
        for r in range(row, m):
            if A[r, col] % p != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        if pivot != row:
            A.row_swap(row, pivot)
        
        inv = pow(int(A[row, col]), -1, p)
        for c in range(col, k + 1):
            A[row, c] = (A[row, c] * inv) % p
            
        for r in range(m):
            if r != row and A[r, col] % p != 0:
                factor = A[r, col]
                for c in range(col, k + 1):
                    A[r, c] = (A[r, c] - factor * A[row, c]) % p
        row += 1
        
    for r in range(m):
        is_zero = True
        for c in range(k):
            if A[r, c] % p != 0:
                is_zero = False
                break
        if is_zero and A[r, k] % p != 0:
            return None
            
    c_sol = []
    for i in range(k):
        c_sol.append(int(A[i, k]) % p)
    return c_sol

def get_minpoly_mod_p(A, p):
    """Computes the minimal polynomial of a square matrix A over GF(p)."""
    n = A.shape[0]
    if n == 0:
        return None
    I = eye(n)
    powers = [I]
    for _ in range(n):
        powers.append((powers[-1] * A).applyfunc(lambda val: val % p))
    
    def flatten(mat):
        return [mat[r, c] % p for r in range(n) for c in range(n)]
    
    vecs = [flatten(mat) for mat in powers]
    
    x = Symbol('x')
    for k in range(1, n + 1):
        M = Matrix(vecs[:k]).T
        v = Matrix(vecs[k])
        
        c = solve_mod_p(M, v, p)
        if c is not None:
            poly = x**k
            for i in range(k):
                poly += ((-c[i]) % p) * x**i
            return Poly(poly, x, domain=GF(p))
    return None

def matrix_power_mod_p(A, power, p):
    """Computes A^power mod p efficiently."""
    n = A.shape[0]
    res = eye(n)
    base = A.copy()
    while power > 0:
        if power % 2 == 1:
            res = (res * base).applyfunc(lambda val: val % p)
        base = (base * base).applyfunc(lambda val: val % p)
        power //= 2
    return res

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: a dictionary {'p': int, 'q': int, 'alpha': matrix_like}
    or a tuple (p, q, alpha).
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
            alpha = witness['alpha']
        else:
            p, q, alpha = witness
    except Exception:
        return [False, False]
        
    # H_1: F_q is a finite field of characteristic p
    h1 = False
    try:
        if isprime(p):
            temp = q
            while temp % p == 0 and temp > 1:
                temp //= p
            if temp == 1 and q >= p:
                h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The minimal polynomial of alpha^q over F_q is NOT the same as the minimal polynomial of alpha over F_q
    neg_q_ok = False
    try:
        A = Matrix(alpha)
        A_q = matrix_power_mod_p(A, q, p)
        
        poly_alpha = get_minpoly_mod_p(A, p)
        poly_alpha_q = get_minpoly_mod_p(A_q, p)
        
        if poly_alpha is not None and poly_alpha_q is not None:
            neg_q_ok = (poly_alpha != poly_alpha_q)
    except Exception:
        neg_q_ok = False
        
    return [h1, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p",
    "¬Q: The minimal polynomial of alpha^q over F_q is NOT the same as the minimal polynomial of alpha over F_q"
]

N_HYP = 1
NEG_Q_INDEX = 1