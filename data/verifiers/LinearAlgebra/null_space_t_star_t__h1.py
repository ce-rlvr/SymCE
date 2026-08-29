import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (T, G) where:
      - T is a square sympy Matrix representing the linear operator.
      - G is a square, invertible, Hermitian sympy Matrix representing the metric tensor 
        (inner product) of the space V, which defines the adjoint T^*.
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False, False]
        T, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: Let T be a linear operator on V.
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False
        
    # H_2: Assume the adjoint operator T^* exists.
    # In a space with metric G, the adjoint exists and is uniquely defined if G is non-degenerate.
    # We also require G to be Hermitian to define a valid inner product space.
    try:
        h2 = isinstance(G, Matrix) and G.is_square and G.shape == T.shape and G == G.H and G.det() != 0
    except Exception:
        h2 = False
        
    # ¬Q: The null space of T^*T is NOT equal to the null space of T.
    try:
        if h1 and h2:
            # Compute the adjoint T^* with respect to the metric G
            # <Tx, y> = <x, T^*y>  =>  y^H G T x = (T^* y)^H G x = y^H (T^*)^H G x
            # => G T = (T^*)^H G  =>  T^* = G^{-1} T^H G
            T_star = G.inv() * T.H * G
            
            null_T = T.nullspace()
            null_T_star_T = (T_star * T).nullspace()
            
            # Compare the spans of the null spaces
            if len(null_T) != len(null_T_star_T):
                neg_q = True
            elif len(null_T) == 0:
                neg_q = False
            else:
                M1 = Matrix.hstack(*null_T)
                M2 = Matrix.hstack(*null_T_star_T)
                M_both = Matrix.hstack(M1, M2)
                # They are equal if the rank of the combined matrix equals the rank of each individual matrix
                spans_equal = (M1.rank() == M_both.rank()) and (M2.rank() == M_both.rank())
                neg_q = not spans_equal
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: The adjoint operator T^* exists",
    "¬Q: The null space of T^*T is not equal to the null space of T"
]

N_HYP = 2
NEG_Q_INDEX = 2