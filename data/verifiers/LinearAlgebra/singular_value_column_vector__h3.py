import sympy
from sympy import Matrix, simplify, I, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    Hypotheses:
      1. v is an m x 1 complex column vector
      2. v is non-zero
    Conclusion:
      The matrix v has exactly one non-zero singular value, which is equal to ||v||_2
    """
    # H_1: Let v be an m x 1 complex column vector
    try:
        h1 = (isinstance(witness, Matrix) and 
              witness.shape[1] == 1 and 
              all(e.is_complex is not False for e in witness))
    except Exception:
        h1 = False

    # H_2: Assume v is non-zero
    try:
        h2 = not witness.is_zero_matrix
    except Exception:
        h2 = False

    # neg_Q: The matrix v does NOT have exactly one non-zero singular value, which is equal to ||v||_2
    try:
        svs = witness.singular_values()
        non_zero_svs = [s for s in svs if simplify(s) != 0]
        
        if len(non_zero_svs) != 1:
            neg_q = True
        else:
            norm_v = witness.norm()
            diff = simplify(non_zero_svs[0] - norm_v)
            neg_q = (diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: v is an m x 1 complex column vector",
    "H_2: v is non-zero",
    "¬Q: v does not have exactly one non-zero singular value equal to ||v||_2"
]

N_HYP = 2
NEG_Q_INDEX = 2