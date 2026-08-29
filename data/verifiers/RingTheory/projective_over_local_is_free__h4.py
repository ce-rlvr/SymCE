import sympy
from sympy import Matrix, eye, zeros
from sympy.ntheory import factorint

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    witness: tuple (n, A)
    where n is an integer >= 2 representing the ring R = Z/nZ,
    and A is a sympy Matrix representing the presentation matrix of the R-module M.
    Specifically, M = R^r / Im(A), where r is the number of rows of A.
    """
    try:
        n, A = witness
        n = int(n)
        if n < 2:
            return [False, False, False, False]
        A = Matrix(A)
        for val in A:
            if not getattr(val, 'is_integer', False):
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a commutative ring
    # Z/nZ is always commutative.
    try:
        h1 = True
    except Exception:
        h1 = False
    
    # H2: R is a local ring
    # Z/nZ is local iff n = p^k for some prime p.
    try:
        factors = factorint(n)
        h2 = (len(factors) == 1)
    except Exception:
        h2 = False
        
    # H3: M is a finitely generated R-module
    # M is presented by a finite matrix A, so it is finitely generated.
    try:
        r = A.rows
        c = A.cols
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: M is NOT a free R-module
    try:
        r = A.rows
        if A.cols == 0:
            M_mat = n * eye(r)
        else:
            M_mat = A.row_join(n * eye(r))
            
        snf = M_mat.smith_normal_form()
        
        is_free = True
        for i in range(min(snf.rows, snf.cols)):
            d = snf[i, i]
            if d not in (1, n):
                is_free = False
                break
                
        neg_q = not is_free
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring",
    "H_3: M is a finitely generated R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3