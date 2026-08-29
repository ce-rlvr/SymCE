import sympy
from sympy.matrices import eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a dictionary, a 6-tuple, or an object with the required attributes.
    Expected fields:
      - W_is_fd_over_F: bool
      - dim_V: dimension of V
      - n: expected dimension of V
      - dim_W: dimension of W
      - m: expected dimension of W
      - dim_bilinear_forms: dimension of the space of bilinear forms V x W -> F
    """
    if isinstance(witness, dict):
        W_is_fd_over_F = witness.get('W_is_fd_over_F', False)
        dim_V = witness.get('dim_V', None)
        n = witness.get('n', None)
        dim_W = witness.get('dim_W', None)
        m = witness.get('m', None)
        dim_bilinear_forms = witness.get('dim_bilinear_forms', None)
    elif isinstance(witness, (list, tuple)) and len(witness) == 6:
        W_is_fd_over_F, dim_V, n, dim_W, m, dim_bilinear_forms = witness
    else:
        try:
            W_is_fd_over_F = getattr(witness, 'W_is_fd_over_F')
            dim_V = getattr(witness, 'dim_V')
            n = getattr(witness, 'n')
            dim_W = getattr(witness, 'dim_W')
            m = getattr(witness, 'm')
            dim_bilinear_forms = getattr(witness, 'dim_bilinear_forms')
        except AttributeError:
            return [False, False, False, False]

    try:
        h1 = bool(W_is_fd_over_F)
    except Exception:
        h1 = False

    try:
        h2 = (dim_V == n) and (n is not None)
    except Exception:
        h2 = False

    try:
        h3 = (dim_W == m) and (m is not None)
    except Exception:
        h3 = False

    try:
        if dim_bilinear_forms is None or n is None or m is None:
            neg_q = False
        else:
            if hasattr(dim_bilinear_forms, 'free_symbols') or hasattr(n, 'free_symbols') or hasattr(m, 'free_symbols'):
                diff = sympy.simplify(dim_bilinear_forms - n * m)
                neg_q = (diff != 0)
            else:
                neg_q = (dim_bilinear_forms != n * m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: W is a finite-dimensional vector space over the field F",
    "H_2: The dimension of V is n",
    "H_3: The dimension of W is m",
    "¬Q: The vector space of all bilinear forms B: V \\times W \\to F does not have dimension nm"
]

N_HYP = 3
NEG_Q_INDEX = 3