import sympy

CONDITION_LABELS = [
    "H_1: k >= 2 is an integer",
    "H_2: tau_k(n) is the Piltz divisor function",
    "H_3: s is a complex number with Re(s) > 1",
    "¬Q: The Dirichlet series of tau_k(n) does not equal zeta(s)^k"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            k = witness.get('k')
            s = witness.get('s')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                k, s = witness[0], witness[1]
            elif len(witness) >= 3:
                k, s = witness[0], witness[-1]
            else:
                k, s = None, None
        else:
            k, s = None, None
    except Exception:
        k, s = None, None

    # H1: k >= 2 is an integer
    try:
        h1 = False
        if k is not None:
            if isinstance(k, (int, sympy.Integer)):
                if k >= 2:
                    h1 = True
            else:
                k_float = float(k)
                if k_float.is_integer() and k_float >= 2:
                    h1 = True
    except Exception:
        h1 = False

    # H2: tau_k(n) is the Piltz divisor function
    # This is a definition, so it holds as long as the witness provides the necessary variables.
    try:
        h2 = False
        if k is not None and s is not None:
            h2 = True
    except Exception:
        h2 = False

    # H3: s is a complex number with Re(s) > 1
    try:
        h3 = False
        if s is not None:
            if isinstance(s, sympy.Expr) and not s.is_number:
                h3 = False
            else:
                s_val = complex(s)
                if s_val.real > 1:
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: The conclusion FAILS
    # The conclusion is mathematically true for all integers k >= 0 and Re(s) > 1.
    # It fails if Re(s) <= 1 (series diverges) or if k is not a non-negative integer.
    try:
        neg_q = True
        if k is not None and s is not None:
            is_k_int = False
            k_val = -1
            if isinstance(k, (int, sympy.Integer)):
                is_k_int = True
                k_val = k
            else:
                try:
                    k_float = float(k)
                    if k_float.is_integer():
                        is_k_int = True
                        k_val = int(k_float)
                except Exception:
                    pass
            
            if is_k_int and k_val >= 0:
                if isinstance(s, sympy.Expr) and not s.is_number:
                    neg_q = False
                else:
                    s_val = complex(s)
                    if s_val.real > 1:
                        neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]