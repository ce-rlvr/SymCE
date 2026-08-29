import sympy
from sympy import Poly, Matrix, eye
from sympy.abc import x
from sympy.ntheory import factorint

def conditions(witness):
    try:
        q, f_expr, Q_matrix = witness
    except Exception:
        return [False, False, False]
    
    # H1: F_q is a finite field with q elements
    try:
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            h1 = len(factorint(q)) == 1
    except Exception:
        h1 = False
        
    # H2: Q is the n x n matrix whose i-th row is the coefficient vector of x^{iq} mod f(x)
    try:
        if not isinstance(Q_matrix, Matrix):
            h2 = False
        else:
            n = Q_matrix.shape[0]
            if Q_matrix.shape[1] != n:
                h2 = False
            else:
                f_poly = Poly(f_expr, x, domain=f'GF({q})')
                h2 = True
                for i in range(n):
                    rem = Poly(x**(i*q), x, domain=f'GF({q})') % f_poly
                    coeffs = rem.all_coeffs()[::-1]
                    if len(coeffs) < n:
                        coeffs.extend([0] * (n - len(coeffs)))
                    elif len(coeffs) > n:
                        coeffs = coeffs[:n]
                    for j in range(n):
                        if (Q_matrix[i, j] - coeffs[j]) % q != 0:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # neg_Q: The number of distinct monic irreducible factors of f(x) over F_q 
    # is NOT equal to the dimension of the null space of Q - I
    try:
        f_poly = Poly(f_expr, x, domain=f'GF({q})')
        factors = f_poly.factor_list()[1]
        num_factors = len(factors)
        
        n = Q_matrix.shape[0]
        Q_minus_I = []
        for i in range(n):
            row = []
            for j in range(n):
                val = Q_matrix[i, j]
                if i == j:
                    val -= 1
                row.append(val % q)
            Q_minus_I.append(row)
            
        rank = 0
        rows = n
        cols = n
        M = [list(row) for row in Q_minus_I]
        
        if len(factorint(q)) == 1 and list(factorint(q).values())[0] == 1:
            for j in range(cols):
                pivot = -1
                for i in range(rank, rows):
                    if M[i][j] % q != 0:
                        pivot = i
                        break
                if pivot != -1:
                    M[rank], M[pivot] = M[pivot], M[rank]
                    inv = 1
                    for inv_cand in range(1, q):
                        if (M[rank][j] * inv_cand) % q == 1:
                            inv = inv_cand
                            break
                    for k in range(cols):
                        M[rank][k] = (M[rank][k] * inv) % q
                    for i in range(rows):
                        if i != rank and M[i][j] % q != 0:
                            factor = M[i][j]
                            for k in range(cols):
                                M[i][k] = (M[i][k] - factor * M[rank][k]) % q
                    rank += 1
            nullity = cols - rank
            neg_q = (num_factors != nullity)
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: Q is the n x n matrix whose i-th row is the coefficient vector of x^{iq} mod f(x)",
    "¬Q: The number of distinct monic irreducible factors of f(x) over F_q is not equal to the dimension of the null space of Q - I"
]

N_HYP = 2
NEG_Q_INDEX = 2