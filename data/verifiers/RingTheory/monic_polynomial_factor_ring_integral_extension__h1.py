import sympy
from sympy import MatrixBase, eye, Poly, zeros
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a polynomial over R",
    "H_2: f is monic",
    "H_3: The degree of f is at least 1",
    "neg_Q: The natural injection does not embed R into the quotient ring or it is not an integral extension"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[1], (list, tuple, MatrixBase)):
                witness = witness[1]
    except Exception:
        pass

    coeffs = None
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            if all(isinstance(c, MatrixBase) for c in witness):
                coeffs = list(witness)
        elif isinstance(witness, MatrixBase):
            free = witness.free_symbols
            if len(free) == 1:
                x_sym = list(free)[0]
                max_deg = -1
                valid = True
                for i in range(witness.rows):
                    for j in range(witness.cols):
                        try:
                            p = Poly(witness[i, j], x_sym)
                            deg = p.degree()
                            if deg > max_deg:
                                max_deg = deg
                        except Exception:
                            valid = False
                if valid and max_deg >= 0:
                    coeffs = []
                    for d in range(max_deg + 1):
                        def get_nth(expr, d=d):
                            try:
                                return Poly(expr, x_sym).nth(d)
                            except Exception:
                                return 0
                        c_mat = witness.applyfunc(get_nth)
                        coeffs.append(c_mat)
            elif len(free) == 0:
                coeffs = [witness]
    except Exception:
        pass

    try:
        if coeffs is not None and len(coeffs) > 0:
            n = coeffs[0].shape[0]
            O = zeros(n, n)
            while len(coeffs) > 1 and coeffs[-1] == O:
                coeffs.pop()
    except Exception:
        pass

    h1 = False
    try:
        if coeffs is not None and len(coeffs) > 0:
            shapes = [c.shape for c in coeffs]
            if all(s[0] == s[1] for s in shapes) and all(s == shapes[0] for s in shapes):
                if shapes[0][0] >= 1:
                    h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if h1:
            n = coeffs[-1].shape[0]
            if coeffs[-1] == eye(n):
                h2 = True
    except Exception:
        pass

    h3 = False
    try:
        if h1:
            if len(coeffs) >= 2:
                h3 = True
    except Exception:
        pass

    neg_q = False
    try:
        if h1:
            from sympy import simplify
            n = coeffs[0].shape[0]
            I = eye(n)
            is_central = True
            for c in coeffs:
                diff = c - c[0, 0] * I
                is_zero = True
                for i in range(n):
                    for j in range(n):
                        if simplify(diff[i, j]) != 0:
                            is_zero = False
                            break
                    if not is_zero:
                        break
                if not is_zero:
                    is_central = False
                    break
            if not is_central:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]