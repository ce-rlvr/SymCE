import sympy
from sympy import Matrix, eye, Poly
from sympy.abc import x

def rank_GF(M_mat, q):
    A = [list(row) for row in M_mat.tolist()]
    n = len(A)
    if n == 0: return 0
    m = len(A[0])
    rank = 0
    for j in range(m):
        pivot = -1
        for i in range(rank, n):
            if A[i][j] % q != 0:
                pivot = i
                break
        if pivot != -1:
            A[rank], A[pivot] = A[pivot], A[rank]
            inv = pow(A[rank][j], q - 2, q)
            for k in range(j, m):
                A[rank][k] = (A[rank][k] * inv) % q
            for i in range(n):
                if i != rank and A[i][j] % q != 0:
                    factor = A[i][j]
                    for k in range(j, m):
                        A[i][k] = (A[i][k] - factor * A[rank][k]) % q
            rank += 1
    return rank

def conditions(witness) -> list[bool]:
    try:
        f, q, Q_mat = witness
    except Exception:
        return [False, False, False]

    try:
        if not isinstance(f, Poly):
            f_poly = Poly(f, x, domain=sympy.GF(q))
        else:
            f_poly = f.set_domain(sympy.GF(q))
            
        n = f_poly.degree()
        f_diff = f_poly.diff(x)
        is_sqf = f_poly.gcd(f_diff).degree() == 0
        
        h1 = bool(f_poly.is_monic and is_sqf and n > 0)
    except Exception:
        h1 = False

    try:
        if not isinstance(Q_mat, Matrix):
            h2 = False
        elif Q_mat.shape != (n, n):
            h2 = False
        else:
            h2 = True
            for i in range(n):
                rem = Poly(1, x, domain=sympy.GF(q))
                base = Poly(x, x, domain=sympy.GF(q))
                exp = i * q
                while exp > 0:
                    if exp % 2 == 1:
                        rem = (rem * base) % f_poly
                    base = (base * base) % f_poly
                    exp //= 2
                
                coeffs = rem.all_coeffs()
                coeffs = coeffs[::-1]
                if len(coeffs) < n:
                    coeffs.extend([0] * (n - len(coeffs)))
                
                row = list(Q_mat.row(i))
                for j in range(n):
                    if (row[j] - coeffs[j]) % q != 0:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    try:
        factors = f_poly.factor_list()
        num_factors = len(factors[1])
        
        I = eye(n)
        Q_minus_I = Q_mat - I
        
        rank = rank_GF(Q_minus_I, q)
        nullity = n - rank
        
        neg_q = bool(num_factors != nullity)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a monic square-free polynomial of degree n in F_q",
    "H_2: Q is the n x n matrix whose i-th row is the coefficient vector of x^{iq} mod f",
    "not_Q: The number of distinct monic irreducible factors of f over F_q is NOT equal to the dimension of the null space of Q - I"
]

N_HYP = 2
NEG_Q_INDEX = 2