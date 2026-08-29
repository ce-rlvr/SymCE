import sympy
from sympy import Matrix
from sympy.ntheory import primefactors
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def matrix_rank_mod_p(M, p):
    """
    Computes the rank of a matrix M over the finite field Z/pZ.
    """
    A = [list(row) for row in M.tolist()]
    rows = len(A)
    cols = len(A[0]) if rows > 0 else 0
    rank = 0
    for c in range(cols):
        pivot = -1
        for r in range(rank, rows):
            if A[r][c] % p != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        # Swap the pivot row into the current rank position
        A[rank], A[pivot] = A[pivot], A[rank]
        # Fermat's Little Theorem for modular inverse
        inv = pow(A[rank][c] % p, p - 2, p)
        # Eliminate entries in the current column for all other rows
        for r in range(rows):
            if r != rank and A[r][c] % p != 0:
                factor = A[r][c]
                for c2 in range(c, cols):
                    A[r][c2] = (A[r][c2] - factor * A[rank][c2] * inv) % p
        rank += 1
    return rank

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the conjecture:
    "Every finitely generated projective module over a commutative ring is free."
    
    The expected witness format is a tuple (n, P) where:
      - n is an integer >= 2, representing the commutative ring R = Z/nZ.
      - P is a square matrix with integer entries, representing an idempotent 
        linear transformation whose image is the module M.
    """
    try:
        n, P_raw = witness
        n = abs(int(n))
        P = Matrix(P_raw)
        if not all(val.is_integer for val in P):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a commutative ring
    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False
        
    # H_2: M is a finitely generated R-module
    try:
        h2 = bool(h1 and P.is_square)
    except Exception:
        h2 = False
        
    # H_3: M is a projective R-module
    # M is projective if P is an idempotent matrix over Z/nZ (i.e., P^2 = P mod n)
    try:
        if h2:
            P2 = P * P
            diff = P2 - P
            h3 = bool(all((val % n) == 0 for val in diff))
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: M is not a free R-module
    # Over Z/nZ, a projective module is free iff its rank is constant across all 
    # localizations at prime ideals (i.e., the rank of P mod p is the same for all p | n).
    try:
        if h3:
            primes = primefactors(n)
            ranks = set()
            for p in primes:
                ranks.add(matrix_rank_mod_p(P, p))
            neg_q = bool(len(ranks) > 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is a finitely generated R-module",
    "H_3: M is a projective R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3