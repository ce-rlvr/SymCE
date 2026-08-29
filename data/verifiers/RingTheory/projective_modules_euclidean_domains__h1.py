import sympy
from sympy import Matrix, eye, zeros
import sympy.ntheory

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def rank_mod_p(M, p):
    """Computes the rank of a matrix over GF(p)."""
    A = [list(row) for row in M.tolist()]
    m, n_cols = len(A), len(A[0])
    rank = 0
    for j in range(n_cols):
        pivot = -1
        for i in range(rank, m):
            if A[i][j] % p != 0:
                pivot = i
                break
        if pivot != -1:
            A[rank], A[pivot] = A[pivot], A[rank]
            inv = pow(int(A[rank][j]), -1, p)
            for i in range(rank + 1, m):
                factor = (A[i][j] * inv) % p
                for k in range(j, n_cols):
                    A[i][k] = (A[i][k] - factor * A[rank][k]) % p
            rank += 1
    return rank

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be a tuple (n, e) representing the ring R = Z/nZ 
    and the module M = Im(e) where e is an idempotent element or matrix over R.
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False]
            
        n, e = witness
        n = int(n)
        if n <= 1:
            return [False, False]
            
        if isinstance(e, (list, tuple)):
            e = Matrix(e)
            
        if isinstance(e, (int, sympy.Integer)):
            e = int(e)
            # H_1: M is a projective module over R (e is idempotent mod n)
            h1 = ((e * e) % n == e % n)
            # Q: M is a free module (for rank 1 idempotents over Z/nZ, e must be 0 or 1)
            is_free = (e % n == 0) or (e % n == 1)
            return [h1, not is_free]
            
        elif isinstance(e, Matrix):
            if not all(isinstance(x, (int, sympy.Integer)) for x in e):
                return [False, False]
                
            e_sq = (e * e).applyfunc(lambda x: x % n)
            e_mod = e.applyfunc(lambda x: x % n)
            
            # H_1: M is a projective module over R (e is idempotent mod n)
            h1 = (e_sq == e_mod)
            
            # Q: M is a free module
            # A projective module over Z/nZ is free iff its rank is constant 
            # across all local components (i.e., over Z/pZ for all p | n).
            factors = sympy.ntheory.factorint(n)
            ranks = set()
            for p in factors:
                ranks.add(rank_mod_p(e_mod, p))
                
            is_free = len(ranks) <= 1
            return [h1, not is_free]
            
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: M is a projective module over R",
    "¬Q: M is not a free module"
]

N_HYP = 1
NEG_Q_INDEX = 1