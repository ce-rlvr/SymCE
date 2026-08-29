import sympy
from sympy import MatrixBase, zeros, eye
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        h2 = h1 and witness.shape[0] >= 2
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            n = witness.shape[0]
            T = witness.trace()
            
            # The conclusion states that:
            # If T != 0, JCF is diag(T, 0, ..., 0)
            # If T == 0, JCF is J_2(0) block and n-2 J_1(0) blocks
            # Both of these are mathematically equivalent to: A^2 = T * A and rank(A) == 1
            
            diff = witness**2 - T * witness
            is_eq = (diff == zeros(n, n))
            if not is_eq:
                is_eq = all(sympy.expand(val) == 0 for val in diff)
                
            conclusion_holds = is_eq and (witness.rank() == 1)
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over an algebraically closed field F",
    "H_2: n >= 2",
    "¬Q: The Jordan canonical form of A does not match the specified block structure"
]

N_HYP = 2
NEG_Q_INDEX = 2