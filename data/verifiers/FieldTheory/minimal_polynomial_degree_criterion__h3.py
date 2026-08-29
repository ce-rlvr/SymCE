import sympy
from sympy import Matrix

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_prime_power(q):
    if not isinstance(q, (int, sympy.Integer)) or q < 2: 
        return False
    f = sympy.factorint(int(q))
    return len(f) == 1

def conditions(witness):
    try:
        q, n, alpha, d = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F_q is a finite field with q elements
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    # H_2: F_{q^n} is an extension field of degree n over F_q
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n >= 1
    except Exception:
        h2 = False
        
    # H_3: d is the smallest positive integer such that alpha^{q^d} = alpha
    try:
        if not isinstance(d, (int, sympy.Integer)) or d < 1:
            h3 = False
        elif not isinstance(alpha, sympy.Matrix):
            h3 = False
        elif alpha.shape[0] < 1 or alpha.shape[0] != alpha.shape[1]:
            h3 = False
        elif not all(isinstance(x, (int, sympy.Integer)) for x in alpha):
            h3 = False
        else:
            # We restrict q to be prime so that matrix operations mod q form a valid F_q algebra
            if not sympy.isprime(int(q)):
                h3 = False
            else:
                h3 = True
                q_int = int(q)
                A_curr = alpha.applyfunc(lambda x: int(x) % q_int)
                alpha_mod = A_curr
                
                def matrix_pow_mod(A, p, mod_q):
                    res = sympy.eye(A.shape[0])
                    base = A
                    exp = int(p)
                    while exp > 0:
                        if exp % 2 == 1:
                            res = (res * base).applyfunc(lambda x: int(x) % mod_q)
                        base = (base * base).applyfunc(lambda x: int(x) % mod_q)
                        exp //= 2
                    return res

                for k in range(1, int(d)):
                    A_curr = matrix_pow_mod(A_curr, q_int, q_int)
                    if A_curr == alpha_mod:
                        h3 = False
                        break
                if h3:
                    A_curr = matrix_pow_mod(A_curr, q_int, q_int)
                    if A_curr != alpha_mod:
                        h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The degree of the minimal polynomial of alpha over F_q is not equal to d
    try:
        if not sympy.isprime(int(q)):
            neg_q_ok = False
        elif not isinstance(alpha, sympy.Matrix) or alpha.shape[0] < 1 or alpha.shape[0] != alpha.shape[1]:
            neg_q_ok = False
        else:
            q_int = int(q)
            m = alpha.shape[0]
            vecs = []
            Ak = sympy.eye(m)
            deg = m
            for k in range(m + 1):
                vec = [int(Ak[i, j]) % q_int for i in range(m) for j in range(m)]
                vecs.append(vec)
                
                M = [list(row) for row in vecs]
                r = len(M)
                c = len(M[0])
                rank = 0
                for j in range(c):
                    pivot = -1
                    for i in range(rank, r):
                        if M[i][j] % q_int != 0:
                            pivot = i
                            break
                    if pivot != -1:
                        M[rank], M[pivot] = M[pivot], M[rank]
                        inv = pow(int(M[rank][j]), -1, q_int)
                        for i in range(rank + 1, r):
                            factor = (M[i][j] * inv) % q_int
                            for col in range(j, c):
                                M[i][col] = (M[i][col] - factor * M[rank][col]) % q_int
                        rank += 1
                if rank < len(vecs):
                    deg = k
                    break
                Ak = (Ak * alpha).applyfunc(lambda x: int(x) % q_int)
            
            neg_q_ok = (deg != int(d))
    except Exception:
        neg_q_ok = False
        
    return [h1, h2, h3, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^n} is an extension field of degree n over F_q",
    "H_3: d is the smallest positive integer such that alpha^{q^d} = alpha",
    "¬Q: The degree of the minimal polynomial of alpha over F_q is not equal to d"
]

N_HYP = 3
NEG_Q_INDEX = 3