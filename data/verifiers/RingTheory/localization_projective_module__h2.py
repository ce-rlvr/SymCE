import sympy
from sympy import Matrix, eye, zeros, gcd, Integer
from sympy.ntheory import factorint
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Expected witness format:
    witness = (R_type, S_gens, P_relations)
    - R_type: str, must be 'Z' (representing the ring of integers)
    - S_gens: list of int, generators of the multiplicatively closed set S
    - P_relations: sympy.Matrix, presentation matrix of the finitely generated module P over Z
                   (i.e., P = Z^n / im(P_relations))
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        R_type, S_gens, M = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    try:
        H1 = (R_type == 'Z')
    except Exception:
        H1 = False
        
    # H_2: S is a multiplicatively closed subset of R
    try:
        H2 = isinstance(S_gens, list) and all(isinstance(s, (int, Integer)) for s in S_gens)
    except Exception:
        H2 = False
        
    # ¬Q: The localized module S^{-1}P is not a projective S^{-1}R-module
    try:
        if not isinstance(M, Matrix) or not all(isinstance(val, (int, Integer)) for val in M):
            neg_Q = False
        elif M.rows > 6 or M.cols > 6:
            # Restrict matrix size to ensure fast verification
            neg_Q = False
        else:
            r = M.rank()
            if r == 0:
                D_r = 1
            else:
                # D_r is the gcd of all r x r minors, which equals the product of all non-zero elementary divisors
                rows = list(range(M.rows))
                cols = list(range(M.cols))
                D_r = 0
                for row_indices in itertools.combinations(rows, r):
                    for col_indices in itertools.combinations(cols, r):
                        subM = M.extract(row_indices, col_indices)
                        det = subM.det()
                        D_r = gcd(D_r, det)
                        if D_r == 1:
                            break
                    if D_r == 1:
                        break
            
            # S^{-1}P is projective over S^{-1}Z iff it is free, which means its torsion is zero.
            # This happens iff all non-zero elementary divisors are units in S^{-1}Z.
            # Equivalently, their product D_r must be a unit in S^{-1}Z.
            if 0 in S_gens:
                is_proj = True  # S^{-1}Z is the zero ring, all modules are projective
            else:
                D_r = abs(D_r)
                if D_r == 1:
                    is_proj = True
                elif D_r == 0:
                    is_proj = False
                else:
                    primes = factorint(D_r).keys()
                    is_proj = True
                    for p in primes:
                        divides = False
                        for s in S_gens:
                            if s != 0 and s % p == 0:
                                divides = True
                                break
                        if not divides:
                            is_proj = False
                            break
            neg_Q = not is_proj
    except Exception:
        neg_Q = False
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized module S^{-1}P is not a projective S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2