import sympy
from sympy import Poly, Symbol
from sympy.matrices import MatrixBase, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def evaluate_p_T(T, p):
    """Evaluates the polynomial p at the linear operator (matrix) T."""
    if callable(p):
        return p(T)
    if isinstance(p, (list, tuple)):
        # p is given as a list of coefficients [a_0, a_1, ..., a_n]
        p_T = T.zeros(T.shape[0], T.shape[1])
        for i, c in enumerate(p):
            term = T**i
            p_T += c * term
        return p_T
    if isinstance(p, Poly):
        coeffs = p.all_coeffs() # [a_n, ..., a_0]
        n = len(coeffs) - 1
        p_T = T.zeros(T.shape[0], T.shape[1])
        for i, c in enumerate(coeffs):
            term = T**(n - i)
            p_T += c * term
        return p_T
    if hasattr(p, 'free_symbols'):
        symbols = list(p.free_symbols)
        if not symbols:
            return p * eye(T.shape[0])
        x = symbols[0]
        poly_p = Poly(p, x)
        coeffs = poly_p.all_coeffs()
        n = len(coeffs) - 1
        p_T = T.zeros(T.shape[0], T.shape[1])
        for i, c in enumerate(coeffs):
            term = T**(n - i)
            p_T += c * term
        return p_T
    if isinstance(p, MatrixBase):
        return p
    if isinstance(p, (int, float)):
        return p * eye(T.shape[0])
    raise ValueError("Unknown polynomial format")

def conditions(witness):
    try:
        T, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: T is a linear operator on V
    try:
        h1 = isinstance(T, MatrixBase) and T.is_square
    except Exception:
        h1 = False
        
    # H_2: p(x) is a polynomial with coefficients in F
    try:
        if callable(p):
            h2 = True
        elif isinstance(p, (list, tuple)):
            h2 = True
        elif isinstance(p, Poly):
            h2 = True
        elif hasattr(p, 'free_symbols'):
            symbols = list(p.free_symbols)
            if not symbols:
                h2 = True
            else:
                x = symbols[0]
                try:
                    Poly(p, x)
                    h2 = True
                except Exception:
                    h2 = False
        elif isinstance(p, MatrixBase):
            h2 = True
        elif isinstance(p, (int, float)):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The image of the operator p(T) is not a T-invariant subspace of V
    try:
        p_T = evaluate_p_T(T, p)
        col_space = p_T.columnspace()
        
        if not col_space:
            # The zero subspace is always T-invariant
            neg_q = False
        else:
            rank_p_T = p_T.rank()
            neg_q = False
            # Check if T(v) is in Im(p(T)) for each basis vector v of Im(p(T))
            for v in col_space:
                Tv = T * v
                augmented = p_T.row_join(Tv)
                if augmented.rank() > rank_p_T:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: p(x) is a polynomial with coefficients in F",
    "¬Q: The image of the operator p(T) is not a T-invariant subspace of V"
]

N_HYP = 2
NEG_Q_INDEX = 2