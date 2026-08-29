import sympy
from sympy.ntheory import factorint
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Expects witness to be a tuple (n, A) where:
      - n is an integer >= 2 representing the ring R = Z/nZ.
      - A is a sympy.Matrix (or list of lists) with integer entries,
        representing the presentation matrix of the R-module M.
        Specifically, M = R^c / Im(A), where c is the number of rows of A.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, A = witness
            
            if isinstance(n, (int, sympy.Integer)):
                if n >= 2:
                    factors = factorint(n)
                    # Z/nZ is a local ring iff n is a prime power
                    if len(factors) == 1:
                        h1 = True
            
            if isinstance(A, list):
                try:
                    A = sympy.Matrix(A)
                except Exception:
                    pass
                    
            if isinstance(A, sympy.Matrix):
                if all(isinstance(val, (int, sympy.Integer)) for val in A):
                    h2 = True
                    
            if h1 and h2:
                c = A.rows
                if c == 0:
                    # M is the zero module, which is free of rank 0
                    neg_q = False
                else:
                    # M as an abelian group is presented by [A | n*I_c]
                    B = A.row_join(n * sympy.eye(c))
                    S = B.smith_normal_form()
                    invariant_factors = [S[i, i] for i in range(c)]
                    
                    # M is a free R-module iff it is isomorphic to (Z/nZ)^k
                    # This happens iff all invariant factors are either 1 (zero factor) or n
                    is_free = all(abs(d) == 1 or abs(d) == n for d in invariant_factors)
                    neg_q = not is_free
                    
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: (R, \mathfrak{m}) is a commutative Noetherian local ring",
    "H_2: M is a finitely generated R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2