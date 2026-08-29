import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    'Preservation of the Radical under Isometry' (with the isometry hypothesis dropped).
    
    The witness is expected to be a tuple of three sympy Matrices: (M_V, M_W, M_T)
    representing the bilinear form on V, the bilinear form on W, and the linear map T.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False] * 5
        M_V, M_W, M_T = witness
    except Exception:
        return [False] * 5

    # H1: V and W are vector spaces over a field F
    try:
        h1 = (isinstance(M_V, Matrix) and isinstance(M_W, Matrix) and isinstance(M_T, Matrix) and
              M_V.shape == M_W.shape == M_T.shape)
    except Exception:
        h1 = False

    # H2: B_V is a bilinear form on V
    try:
        h2 = bool(h1 and M_V.is_square)
    except Exception:
        h2 = False

    # H3: B_W is a bilinear form on W
    try:
        h3 = bool(h1 and M_W.is_square)
    except Exception:
        h3 = False

    # H4: T is a bijective linear map from V to W
    try:
        h4 = bool(h1 and M_T.is_square and M_T.det() != 0)
    except Exception:
        h4 = False

    # neg_Q: The image of the left radical of B_V under T is exactly the left radical of B_W (must FAIL)
    try:
        if not (h1 and h2 and h3 and h4):
            neg_q = False
        else:
            # The left radical of a bilinear form represented by M is the left nullspace of M,
            # which is the nullspace of M^T.
            rad_V = M_V.transpose().nullspace()
            rad_W = M_W.transpose().nullspace()
            
            # Image of rad_V under T
            img_rad_V = [M_T * v for v in rad_V]
            
            # Check if the span of img_rad_V equals the span of rad_W
            if len(img_rad_V) != len(rad_W):
                spans_equal = False
            elif len(img_rad_V) == 0:
                spans_equal = True
            else:
                # Concatenate the basis vectors of both spaces
                M_concat = Matrix.hstack(*(img_rad_V + rad_W))
                # If the spans are equal, the rank of the concatenated matrix will equal the dimension of rad_W
                spans_equal = (M_concat.rank() == len(rad_W))
                
            neg_q = not spans_equal
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: B_V is a bilinear form on V",
    "H_3: B_W is a bilinear form on W",
    "H_4: T is a bijective linear map from V to W",
    "¬Q: The image of the left radical of B_V under T is not exactly the left radical of B_W"
]

N_HYP = 4
NEG_Q_INDEX = 4