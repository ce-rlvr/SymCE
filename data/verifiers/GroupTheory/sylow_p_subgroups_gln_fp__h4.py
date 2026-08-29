import sympy
from sympy.matrices import Matrix, eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                p, n, G = witness
                U_given = None
            elif len(witness) == 4:
                p, n, G, U_given = witness
            else:
                return [False] * 4 + [False]
        else:
            return [False] * 4 + [False]
    except Exception:
        return [False] * 4 + [False]

    # H1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H3: F_p is the finite field of p elements (G is a group of n x n matrices over F_p)
    try:
        h3 = False
        G_set = set()
        if h1 and h2 and isinstance(G, (list, tuple, set)):
            valid_matrices = True
            for M in G:
                if hasattr(M, 'shape') and M.shape == (n, n):
                    tup = tuple(tuple(int(M[i, j]) % p for j in range(n)) for i in range(n))
                elif isinstance(M, (list, tuple)) and len(M) == n and all(isinstance(row, (list, tuple)) and len(row) == n for row in M):
                    tup = tuple(tuple(int(M[i][j]) % p for j in range(n)) for i in range(n))
                else:
                    valid_matrices = False
                    break
                G_set.add(tup)
            
            if valid_matrices and len(G_set) > 0:
                I = tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
                if I in G_set:
                    closed = True
                    for A in G_set:
                        for B in G_set:
                            C = tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) % p for j in range(n)) for i in range(n))
                            if C not in G_set:
                                closed = False
                                break
                        if not closed:
                            break
                    if closed:
                        is_group_flag = True
                        for A in G_set:
                            has_inv = False
                            for B in G_set:
                                C = tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) % p for j in range(n)) for i in range(n))
                                if C == I:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_group_flag = False
                                break
                        if is_group_flag:
                            h3 = True
    except Exception:
        h3 = False

    # H4: U is the subgroup of G consisting of all upper unitriangular matrices
    try:
        h4 = False
        U_calc = set()
        if h3:
            for M in G_set:
                is_uu = True
                for i in range(n):
                    for j in range(n):
                        if i == j and M[i][j] != 1:
                            is_uu = False
                        elif i > j and M[i][j] != 0:
                            is_uu = False
                if is_uu:
                    U_calc.add(M)
            
            if U_given is not None:
                U_given_set = set()
                for M in U_given:
                    if hasattr(M, 'shape') and M.shape == (n, n):
                        tup = tuple(tuple(int(M[i, j]) % p for j in range(n)) for i in range(n))
                    elif isinstance(M, (list, tuple)) and len(M) == n and all(isinstance(row, (list, tuple)) and len(row) == n for row in M):
                        tup = tuple(tuple(int(M[i][j]) % p for j in range(n)) for i in range(n))
                    else:
                        tup = None
                    if tup is not None:
                        U_given_set.add(tup)
                if U_given_set == U_calc:
                    h4 = True
            else:
                h4 = True
            
            if h4:
                closed = True
                for A in U_calc:
                    for B in U_calc:
                        C = tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) % p for j in range(n)) for i in range(n))
                        if C not in U_calc:
                            closed = False
                            break
                    if not closed:
                        break
                h4 = closed
    except Exception:
        h4 = False

    # neg_Q: U is NOT a Sylow p-subgroup of G
    try:
        neg_q = False
        if h3 and h4:
            order_G = len(G_set)
            p_power = 1
            temp = order_G
            while temp > 0 and temp % p == 0:
                p_power *= p
                temp //= p
            
            order_U = len(U_calc)
            if order_U != p_power:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "H_3: F_p is the finite field of p elements",
    "H_4: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4