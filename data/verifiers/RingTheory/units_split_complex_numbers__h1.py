import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: S is the ring of split-complex numbers over R",
    "H_2: a and b are in R",
    "¬Q: a + bj is a unit in S iff a^2 - b^2 is a unit in R is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False]
    
    # H_1: S is the ring of split-complex numbers over R
    # This is a definitional context hypothesis, so it holds by definition.
    h1 = True
    
    # H_2: a, b \in R
    try:
        if hasattr(a, 'is_Matrix') and a.is_Matrix:
            h2 = hasattr(b, 'is_Matrix') and b.is_Matrix and a.shape == b.shape and a.shape[0] == a.shape[1]
        else:
            # Check if they are compatible scalars/elements that can be added and multiplied
            _ = a + b
            _ = a * b
            h2 = not (hasattr(b, 'is_Matrix') and b.is_Matrix)
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion "a + bj is a unit in S iff a^2 - b^2 is a unit in R" FAILS
    try:
        if hasattr(a, 'is_Matrix') and a.is_Matrix:
            # For a matrix ring over a field (where 1/2 exists), S is isomorphic to R x R.
            # Thus, a + bj is a unit in S iff both a + b and a - b are units in R.
            # A matrix is a unit in R iff its determinant is non-zero.
            unit_S = (a + b).det() != 0 and (a - b).det() != 0
            unit_R = (a**2 - b**2).det() != 0
            neg_q = bool(unit_S != unit_R)
        else:
            # The conjecture is true for commutative rings, so no scalar counterexample exists.
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]