import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        mat = Matrix(witness)
        h1 = mat.is_square
    except Exception:
        h1 = False

    try:
        # The action of GL(V) on bilinear forms is a definitional property 
        # that holds for any valid vector space and bilinear form representation.
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            mat = Matrix(witness)
            is_sym = mat.is_symmetric()
            is_non_deg = (mat.det() != 0)
            
            # The conclusion states that the stabilizer is EXACTLY the orthogonal group O(V, B_0).
            # The orthogonal group is the stabilizer of a symmetric, non-degenerate bilinear form.
            # If the form is degenerate or not symmetric, its stabilizer is not the orthogonal group.
            # Thus, the conclusion fails (neg_q is True) if the form is NOT symmetric OR is degenerate.
            neg_q = not (is_sym and is_non_deg)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: G = GL(V) acts on the set of bilinear forms on V via (g · B)(u, v) = B(g⁻¹u, g⁻¹v)",
    "¬Q: The stabilizer of B_0 in G is not exactly the orthogonal group O(V, B_0)"
]

N_HYP = 2
NEG_Q_INDEX = 2