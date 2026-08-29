import sympy
from sympy import Matrix, eye, zeros
from itertools import combinations

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "If T is a linear operator and T^2 = 0, then rank(T) <= dim(V) / 2"
    
    The witness can be a sympy Matrix (assumed over a field of characteristic 0),
    or a tuple (Matrix, mod) representing a matrix over the ring Z/mod Z.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M, mod = witness
        else:
            M = witness
            mod = 0
            
        if not (hasattr(M, 'rows') and hasattr(M, 'cols') and hasattr(M, 'extract')):
            return [False, False, False]
            
        n = M.rows
        h1 = (M.cols == n and n > 0)
        if not h1:
            return [False, False, False]
            
        M2 = M * M
        
        if mod > 1:
            h2 = all(val % mod == 0 for val in M2)
            
            def rank_mod(mat, m):
                for k in range(n, 0, -1):
                    for rows in combinations(range(n), k):
                        for cols in combinations(range(n), k):
                            submat = mat.extract(rows, cols)
                            if submat.det() % m != 0:
                                return k
                return 0
            
            r = rank_mod(M, mod)
            neg_q = r > n / 2
            return [bool(h1), bool(h2), bool(neg_q)]
        else:
            h2 = M2.is_zero_matrix
            neg_q = M.rank() > n / 2
            return [bool(h1), bool(h2), bool(neg_q)]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V (represented as a square matrix)",
    "H_2: T^2 = 0",
    "¬Q: rank(T) > dim(V) / 2"
]

N_HYP = 2
NEG_Q_INDEX = 2