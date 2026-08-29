import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (T, v) where T is a sympy Matrix 
    representing a linear transformation in GL(V) and v is a sympy Matrix 
    representing a non-zero column vector in V.
    """
    try:
        T, v = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: V is a vector space over a field F (implicit, check T is a square matrix)
    try:
        h1_ok = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1_ok = False

    # H2: T is in GL(V) (T is invertible)
    try:
        h2_ok = h1_ok and T.det() != 0
    except Exception:
        h2_ok = False

    # H3: v is a non-zero vector in V
    try:
        h3_ok = isinstance(v, Matrix) and v.shape[1] == 1 and not v.is_zero
    except Exception:
        h3_ok = False

    # H4: T and v have compatible dimensions
    try:
        h4_ok = h1_ok and h3_ok and T.shape[1] == v.shape[0]
    except Exception:
        h4_ok = False

    # neg_Q: The conclusion FAILS at the witness.
    # Conclusion: T stabilizes L iff v is an eigenvector of T.
    # Negation: T stabilizes L XOR v is an eigenvector of T.
    try:
        if not h4_ok:
            neg_q_ok = False
        else:
            Tv = T * v
            # T stabilizes L = span(v) iff Tv is a scalar multiple of v
            # Since v != 0, this is equivalent to the rank of [Tv, v] being 1
            M = Tv.row_join(v)
            stabilizes_L = (M.rank() == 1)
            
            # v is an eigenvector of T iff Tv = lambda * v for some scalar lambda
            # This is mathematically identical to Tv being a scalar multiple of v
            is_eigenvector = (M.rank() == 1)
            
            neg_q_ok = stabilizes_L != is_eigenvector
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: T is a square matrix representing a linear transformation on V",
    "H_2: T is in GL(V) (T is invertible)",
    "H_3: v is a non-zero column vector in V",
    "H_4: T and v have compatible dimensions",
    "¬Q: T stabilizes L XOR v is an eigenvector of T"
]

N_HYP = 4
NEG_Q_INDEX = 4