import sympy
from sympy import Symbol, QQ, I, Rational, degree, roots

x = Symbol('x')

def conditions(witness) -> list[bool]:
    f_expr = None
    E = None
    
    # Unpack witness
    if isinstance(witness, tuple) and len(witness) == 2:
        f, E = witness
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
    else:
        E = witness
        f_expr = x**4 - 2
        
    try:
        if isinstance(E, (list, tuple, set)):
            E = QQ.algebraic_field(*E)
    except Exception:
        pass

    # H_1: f(x) = x^4 - 2
    try:
        h1 = bool(f_expr == x**4 - 2)
    except Exception:
        h1 = False

    # Determine extension degree
    try:
        if E == QQ:
            ext_dim = 1
        elif hasattr(E, 'ext_dim'):
            ext_dim = E.ext_dim
        else:
            ext_dim = None
    except Exception:
        ext_dim = None

    # H_2: E is the splitting field of f(x) over Q
    try:
        if ext_dim is None:
            h2 = False
        elif h1:
            # Fast path for f(x) = x^4 - 2
            try:
                E(2**Rational(1,4))
                E(I)
                h2 = (ext_dim == 8)
            except Exception:
                h2 = False
        else:
            # General path for other polynomials
            rts = roots(f_expr, x)
            if sum(rts.values()) < degree(f_expr, x):
                h2 = False
            else:
                contains_all = True
                for r in rts:
                    try:
                        if E == QQ:
                            if r not in QQ:
                                contains_all = False
                                break
                        else:
                            E(r)
                    except Exception:
                        contains_all = False
                        break
                if contains_all:
                    if not rts:
                        h2 = (ext_dim == 1)
                    else:
                        E_split = QQ.algebraic_field(*rts.keys())
                        h2 = (ext_dim == E_split.ext_dim)
                else:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: The degree of the extension E over Q is not 8
    try:
        if ext_dim is not None:
            q = (ext_dim == 8)
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = x^4 - 2",
    "H_2: E is the splitting field of f(x) over Q",
    "¬Q: The degree of the extension E over Q is not 8"
]

N_HYP = 2
NEG_Q_INDEX = 2