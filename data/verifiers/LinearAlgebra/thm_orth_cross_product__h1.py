import sympy
from sympy import eye, zeros, Matrix

# Top-level setup for potential witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Q is an orthogonal matrix
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            h1_ok = False
        else:
            n = witness.shape[0]
            diff = witness.transpose() * witness - eye(n)
            h1_ok = all(sympy.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
    except Exception:
        h1_ok = False

    # H_2: det(Q) == 1
    try:
        h2_ok = sympy.simplify(witness.det() - 1) == 0
    except Exception:
        h2_ok = False

    # ¬Q: Conclusion fails (Q does not preserve cross products in R^3)
    try:
        def check_conclusion(Q):
            # The conclusion specifically states "For all vectors u and v in R^3..."
            # If Q is not a 3x3 matrix, the operation Q(u x v) is undefined for R^3 vectors.
            if not hasattr(Q, 'shape') or len(Q.shape) != 2:
                return False
            if Q.shape[0] != 3 or Q.shape[1] != 3:
                return False
            
            e1 = Matrix([1, 0, 0])
            e2 = Matrix([0, 1, 0])
            e3 = Matrix([0, 0, 1])
            
            # Check preservation of cross product on the standard basis
            for u in [e1, e2, e3]:
                for v in [e1, e2, e3]:
                    left = Q * u.cross(v)
                    right = (Q * u).cross(Q * v)
                    diff = left - right
                    if not all(sympy.simplify(diff[i, 0]) == 0 for i in range(3)):
                        return False
            return True
            
        neg_q_ok = not check_conclusion(witness)
    except Exception:
        # If any operation fails (e.g., dimension mismatch), the conclusion is false.
        neg_q_ok = True

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "H_2: det(Q) == 1",
    "¬Q: Q does not preserve cross products in R^3"
]

N_HYP = 2
NEG_Q_INDEX = 2