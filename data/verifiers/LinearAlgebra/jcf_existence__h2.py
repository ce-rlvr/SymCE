import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis from the true theorem is "T is a linear operator on V".
    A valid counterexample witness must provide a vector space V (or its dimension) 
    and a matrix T such that T is NOT a valid linear operator on V (e.g., dimensions mismatch),
    but T's characteristic polynomial still splits completely.
    """
    try:
        # Parse witness: expect a tuple (V_dim, T) or (T, V_dim), or a dict/object.
        if isinstance(witness, dict):
            V_dim = witness.get('V_dim', witness.get('V'))
            T = witness.get('T')
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], sympy.MatrixBase):
                T, V_dim = witness
            else:
                V_dim, T = witness
        else:
            V_dim = witness.V
            T = witness.T
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    try:
        if isinstance(V_dim, int):
            dim = V_dim
        elif hasattr(V_dim, 'shape'):
            dim = V_dim.shape[0]
        elif hasattr(V_dim, '__len__'):
            dim = len(V_dim)
        else:
            dim = int(V_dim)
        h1_ok = dim >= 0
    except Exception:
        h1_ok = False

    # H_2: The characteristic polynomial of T splits completely into linear factors over F
    try:
        if not isinstance(T, sympy.MatrixBase) or T.shape[0] != T.shape[1]:
            h2_ok = False
        else:
            x = sympy.Symbol('x')
            cp = T.charpoly(x)
            factors = sympy.factor_list(cp.as_expr())
            h2_ok = all(f.as_poly(x).degree() == 1 for f, mult in factors[1])
    except Exception:
        h2_ok = False

    # ¬Q: There does NOT exist a basis for V such that the matrix of T relative to this basis is in Jordan canonical form.
    # This happens if T cannot act on V (dimensions mismatch) or if T lacks a JCF.
    try:
        if not isinstance(T, sympy.MatrixBase) or T.shape[0] != T.shape[1]:
            q = False
        elif dim != T.shape[0]:
            q = False
        else:
            # If T is a valid operator on V, it has a JCF iff its characteristic polynomial splits completely.
            x = sympy.Symbol('x')
            cp = T.charpoly(x)
            factors = sympy.factor_list(cp.as_expr())
            q = all(f.as_poly(x).degree() == 1 for f, mult in factors[1])
    except Exception:
        q = False

    neg_q_ok = not q

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: The characteristic polynomial of T splits completely into linear factors over F",
    "¬Q: There does not exist a basis for V such that the matrix of T relative to this basis is in Jordan canonical form"
]

N_HYP = 2
NEG_Q_INDEX = 2