import sympy

x = sympy.Symbol('x')
I = sympy.I
pi = sympy.pi
exp = sympy.exp

def conditions(witness):
    h1 = False
    q = False

    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n, zeta = witness
            else:
                n = None
                zeta = None
        else:
            n = witness
            try:
                if n == int(n) and n != 0:
                    zeta = sympy.exp(2 * sympy.I * sympy.pi / abs(int(n)))
                else:
                    zeta = None
            except Exception:
                zeta = None
    except Exception:
        n = None
        zeta = None

    try:
        if n is not None and zeta is not None:
            try:
                is_int = (n == int(n))
            except Exception:
                is_int = False
            if is_int and n != 0:
                abs_n = abs(int(n))
                mp = sympy.minpoly(zeta, x)
                cp = sympy.cyclotomic_poly(abs_n, x)
                h1 = bool(sympy.simplify(mp - cp) == 0)
    except Exception:
        h1 = False

    try:
        if zeta is not None and n is not None:
            mp = sympy.minpoly(zeta, x)
            deg_ext = sympy.degree(mp, x)
            try:
                is_pos_int = (n == int(n) and n > 0)
            except Exception:
                is_pos_int = False
            
            if is_pos_int:
                expected_deg = sympy.totient(int(n))
                q = bool(deg_ext == expected_deg)
            else:
                q = False
        else:
            q = False
    except Exception:
        q = False

    neg_q = not q
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity in C",
    "not Q: The degree of the extension Q(zeta_n) over Q is not exactly phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1