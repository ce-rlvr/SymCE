import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup
from itertools import permutations

S3 = SymmetricGroup(3)
I2 = sp.eye(2)

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: X is an n x n matrix of algebraically independent variables over K",
    "¬Q: The permanent polynomial perm(X) is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    try:
        p = 0
        if isinstance(witness, tuple):
            if isinstance(witness[0], sp.Matrix):
                X_mat = witness[0]
                n = X_mat.shape[0]
                if len(witness) > 1:
                    p = int(witness[1])
            else:
                n = int(witness[0])
                p = int(witness[1])
                X_mat = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'x_{i}_{j}'))
        elif isinstance(witness, sp.Matrix):
            X_mat = witness
            n = X_mat.shape[0]
        else:
            n = int(witness)
            X_mat = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'x_{i}_{j}'))

        h1 = (n >= 2)

        if h1:
            symbols = set()
            h2 = True
            for i in range(n):
                for j in range(n):
                    elem = X_mat[i, j]
                    if not isinstance(elem, sp.Symbol):
                        h2 = False
                    symbols.add(elem)
            if len(symbols) != n * n:
                h2 = False
        else:
            h2 = False
            
    except Exception:
        h1 = False
        h2 = False

    try:
        if h1 and h2:
            perm = 0
            for p_perm in permutations(range(n)):
                term = 1
                for i in range(n):
                    term *= X_mat[i, p_perm[i]]
                perm += term
            
            if p > 0:
                factors = sp.factor_list(perm, modulus=p)
            else:
                factors = sp.factor_list(perm)
                
            is_irreducible = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]