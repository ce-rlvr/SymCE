import sympy
from sympy import Matrix, eye, expand, zeros, Symbol
from itertools import combinations

# Top-level setup: named object bindings for the witness expression
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Non-commutative symbols are provided because the theorem implicitly assumes a commutative field.
# Over a non-commutative ring, the determinant is not multiplicative, providing a counterexample.
x, y, z = sympy.symbols('x y z', commutative=False)
a, b, c = sympy.symbols('a b c')

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness can be a custom object with methods, or a tuple (T, W) where T and W are SymPy matrices.
    """
    # 1. Duck-typing for custom infinite-dimensional or specialized witness objects
    if hasattr(witness, 'is_linear_operator') and hasattr(witness, 'is_invariant'):
        try:
            h1 = bool(witness.is_linear_operator())
            h2 = bool(witness.is_invariant())
            if hasattr(witness, 'check_conclusion'):
                conclusion = bool(witness.check_conclusion())
            elif hasattr(witness, 'det_T') and hasattr(witness, 'det_T_W') and hasattr(witness, 'det_T_quotient'):
                conclusion = (witness.det_T() == witness.det_T_W() * witness.det_T_quotient())
            else:
                conclusion = True
            return [h1, h2, not conclusion]
        except Exception:
            pass

    # 2. Matrix tuple evaluation
    try:
        T, W = witness
        if isinstance(W, list):
            W = Matrix.hstack(*W) if W else zeros(T.shape[0], 0)
    except Exception:
        return [False, False, False]

    # H_1: T is a linear operator on V (T must be a square matrix)
    try:
        h1 = (T.shape[0] == T.shape[1])
    except Exception:
        h1 = False

    # H_2: W is a subspace of V that is invariant under T
    try:
        n, k = W.shape
        if T.shape[0] != n:
            h2 = False
        else:
            A = None
            # Find k linearly independent rows to solve for A in T*W = W*A
            for indices in combinations(range(n), k):
                W_sub = W[list(indices), :]
                if expand(W_sub.det()) != 0:
                    TW_sub = (T * W)[list(indices), :]
                    A = W_sub.inv() * TW_sub
                    break
            
            if A is None:
                h2 = False
            else:
                diff = expand(T * W - W * A)
                h2 = all(diff[i, j] == 0 for i in range(diff.shape[0]) for j in range(diff.shape[1]))
    except Exception:
        h2 = False

    # ¬Q: The determinant of T is NOT equal to det(T|_W) * det(T/W)
    try:
        if not h2:
            neg_q = False
        else:
            I = eye(n)
            P = None
            # Extend W to a basis of V to find the quotient matrix C
            for indices in combinations(range(n), n - k):
                U = I[:, list(indices)]
                test_P = Matrix.hstack(W, U)
                if expand(test_P.det()) != 0:
                    P = test_P
                    break
            
            if P is None:
                neg_q = False
            else:
                P_inv = P.inv()
                P_inv_T_P = expand(P_inv * T * P)
                C = P_inv_T_P[k:, k:]
                
                det_T = T.det()
                det_A = A.det() if A.shape[0] > 0 else 1
                det_C = C.det() if C.shape[0] > 0 else 1
                
                diff_det = expand(det_T - det_A * det_C)
                conclusion = (diff_det == 0)
                neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: W is a subspace of V that is invariant under T",
    "¬Q: The determinant of T is not equal to the product of the determinant of the restriction operator T|_W and the determinant of the quotient operator T/W"
]

N_HYP = 2
NEG_Q_INDEX = 2