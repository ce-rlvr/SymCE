import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: W is a subspace of V",
    "H_3: P_W is the orthogonal projection operator onto W",
    "¬Q: W is invariant under T XOR P_W T P_W = T P_W"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract T, W, P_W from the witness
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            W = witness.get('W')
            P_W = witness.get('P_W')
        else:
            T = getattr(witness, 'T', None)
            W = getattr(witness, 'W', None)
            P_W = getattr(witness, 'P_W', None)
            
        if T is None or W is None or P_W is None:
            T, W, P_W = witness
    except Exception:
        return [False, False, False, False]

    # Normalize inputs to sympy Matrices
    try:
        if not hasattr(T, 'is_square'):
            T = sp.Matrix(T)
        if not hasattr(P_W, 'is_square'):
            P_W = sp.Matrix(P_W)
        if not hasattr(W, 'rows'):
            if isinstance(W, list) and len(W) > 0 and isinstance(W[0], sp.Matrix):
                W = sp.Matrix.hstack(*W)
            else:
                W = sp.Matrix(W)
    except Exception:
        pass

    # H_1: T is a linear operator on V
    try:
        h1 = hasattr(T, 'is_square') and T.is_square
    except Exception:
        h1 = False

    # H_2: W is a subspace of V
    try:
        # W is represented as a matrix whose columns span the subspace
        h2 = hasattr(W, 'rows') and W.rows == T.rows
    except Exception:
        h2 = False

    # H_3: P_W is the orthogonal projection operator onto W
    try:
        h3 = False
        if hasattr(P_W, 'is_square') and P_W.is_square and P_W.rows == T.rows:
            # Orthogonal projection must be symmetric (Hermitian) and idempotent
            sym = (P_W == P_W.H)
            idem = (P_W * P_W == P_W)
            # Its column space must be exactly the subspace W
            col_space = (P_W * W == W) and (P_W.rank() == W.rank())
            h3 = sym and idem and col_space
    except Exception:
        h3 = False

    # ¬Q: Negation of "W is invariant under T if and only if P_W T P_W = T P_W"
    try:
        # W is invariant under T iff T(W) is contained in W
        # Since P_W projects onto W, this is equivalent to P_W * (T * W) == T * W
        is_invariant = (P_W * T * W == T * W)
        
        # The operator equation P_W T P_W = T P_W
        eq = (P_W * T * P_W == T * P_W)
        
        # The conclusion Q is the equivalence of the two
        Q = (is_invariant == eq)
        
        # We return True if the conclusion FAILS
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]