import sympy
from sympy import symbols, Rational, Integer

x, y, z = symbols('x y z')

def get_val(witness, attrs):
    if isinstance(witness, dict):
        for attr in attrs:
            if attr in witness:
                return witness[attr]
    else:
        for attr in attrs:
            if hasattr(witness, attr):
                return getattr(witness, attr)
    return None

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(get_val(witness, ['is_m_adic_completion', 'm_adic_completion']))
    except Exception:
        h1 = False

    try:
        r_dim = get_val(witness, ['R_dim', 'dim_R', 'krull_dim_R'])
        r_hat_dim = get_val(witness, ['R_hat_dim', 'dim_R_hat', 'krull_dim_R_hat'])
        if r_dim is not None and r_hat_dim is not None:
            neg_q = (r_dim != r_hat_dim)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_hat is the m-adic completion of R",
    "¬Q: The Krull dimension of R_hat is not equal to the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1