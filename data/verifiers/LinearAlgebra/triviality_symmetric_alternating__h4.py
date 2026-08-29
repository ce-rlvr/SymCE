import sympy
from sympy.matrices import MatrixBase, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_val(val):
    if val == 0:
        return True
    if hasattr(val, 'is_zero') and val.is_zero:
        return True
    try:
        return sympy.simplify(val) == 0
    except Exception:
        return False

def is_zero_mat(M):
    return all(is_zero_val(x) for x in M)

def conditions(witness):
    # H1: V is a vector space over a field F
    # We represent the bilinear form as a square matrix over a field.
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H2: The characteristic of F is not equal to 2
    try:
        h2 = False
        if h1:
            is_char_2 = False
            for x in witness:
                # Check for explicit modulo 2 arithmetic or GF(2) elements
                if type(x).__name__ == 'GaloisFieldElement' and getattr(x, 'p', None) == 2:
                    is_char_2 = True
                if hasattr(x, 'is_Mod') and x.is_Mod and len(x.args) == 2 and x.args[1] == 2:
                    is_char_2 = True
                if hasattr(x, 'domain') and getattr(x.domain, 'char', None) == 2:
                    is_char_2 = True
            h2 = not is_char_2
    except Exception:
        h2 = False

    # H3: B is a bilinear form on V
    # A square matrix uniquely defines a bilinear form on V = F^n
    try:
        h3 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h3 = False

    # H4: B is alternating
    # A bilinear form is alternating iff its matrix is skew-symmetric and has a zero diagonal.
    try:
        h4 = False
        if h1:
            n = witness.rows
            skew = witness + witness.T
            is_skew = is_zero_mat(skew)
            zero_diag = all(is_zero_val(witness[i, i]) for i in range(n))
            h4 = bool(is_skew and zero_diag)
    except Exception:
        h4 = False

    # neg_Q: B(x,y) = 0 for all x, y \in V FAILS
    # i.e., the bilinear form is NOT the zero form.
    try:
        neg_q = False
        if h1:
            neg_q = not is_zero_mat(witness)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: The characteristic of F is not equal to 2",
    "H_3: B is a bilinear form on V",
    "H_4: B is alternating",
    "¬Q: B is not the zero bilinear form"
]

N_HYP = 4
NEG_Q_INDEX = 4