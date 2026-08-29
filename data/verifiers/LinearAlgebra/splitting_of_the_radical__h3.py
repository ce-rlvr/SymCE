import sympy
from sympy import Matrix
import itertools
import math

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M, p = witness
        else:
            M = witness
            p = 2
            
        if not hasattr(M, 'shape') or M.shape[0] != M.shape[1]:
            return [False, False, False]
            
        n = M.shape[0]
        
        # H_1: V is a finite-dimensional vector space over a field F
        try:
            h1 = sympy.isprime(p)
        except Exception:
            h1 = False
            
        # H_2: B is a symmetric bilinear form on V
        try:
            M_int = [[int(M[i, j]) % p for j in range(n)] for i in range(n)]
            h2 = True
            for i in range(n):
                for j in range(n):
                    if M_int[i][j] != M_int[j][i]:
                        h2 = False
                        break
        except Exception:
            h2 = False
            
        # neg_Q: There does not exist a subspace U such that V = R \oplus U and B|_U is non-degenerate
        try:
            if p < 2:
                neg_q = False
            else:
                M_int = [[int(M[i, j]) % p for j in range(n)] for i in range(n)]
                
                # Find the radical R (null space of M)
                null_vecs = []
                for vec in itertools.product(range(p), repeat=n):
                    is_null = True
                    for i in range(n):
                        val = sum(M_int[i][j] * vec[j] for j in range(n)) % p
                        if val != 0:
                            is_null = False
                            break
                    if is_null:
                        null_vecs.append(tuple(vec))
                        
                null_vecs_set = set(null_vecs)
                dim_R = int(round(math.log(len(null_vecs_set), p)))
                k = n - dim_R
                
                if k == 0:
                    # R = V, U = {0}. B|_U is trivially non-degenerate.
                    neg_q = False
                else:
                    all_vecs = list(itertools.product(range(p), repeat=n))
                    found_U = False
                    
                    # Iterate over all possible bases for a complement U of dimension k
                    for basis_U in itertools.combinations(all_vecs, k):
                        # Check if basis_U is linearly independent
                        span_U = set()
                        for coeffs in itertools.product(range(p), repeat=k):
                            v = tuple(sum(c * basis_U[i][j] for i, c in enumerate(coeffs)) % p for j in range(n))
                            span_U.add(v)
                        if len(span_U) < p**k:
                            continue
                            
                        # Check if U \cap R = {0}
                        if len(span_U.intersection(null_vecs_set)) > 1:
                            continue
                            
                        # Check if B|_U is non-degenerate
                        M_U_entries = []
                        for i in range(k):
                            row = []
                            for j in range(k):
                                val = 0
                                for x in range(n):
                                    for y in range(n):
                                        val += basis_U[i][x] * M_int[x][y] * basis_U[j][y]
                                row.append(val % p)
                            M_U_entries.append(row)
                        
                        M_U = Matrix(M_U_entries)
                        if M_U.det() % p != 0:
                            found_U = True
                            break
                            
                    neg_q = not found_U
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a symmetric bilinear form on V",
    "¬Q: There does not exist a subspace U such that V = R \\oplus U and B|_U is non-degenerate"
]
N_HYP = 2
NEG_Q_INDEX = 2