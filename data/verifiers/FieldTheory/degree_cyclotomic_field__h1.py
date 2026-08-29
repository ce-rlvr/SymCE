import sympy
from sympy import I, pi, exp, Symbol
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, zeta = witness
        else:
            n = witness
            if n == 0:
                zeta = 2
            else:
                zeta = sympy.exp(2 * sympy.I * sympy.pi / n)
    except Exception:
        return [False, False]

    h1 = False
    try:
        n_int = int(n)
        if n == n_int:
            if sympy.simplify(zeta**n_int - 1) == 0:
                h1 = True
                if n_int > 0:
                    for k in range(1, n_int):
                        if sympy.simplify(zeta**k - 1) == 0:
                            h1 = False
                            break
                elif n_int < 0:
                    for k in range(n_int + 1, 0):
                        if sympy.simplify(zeta**k - 1) == 0:
                            h1 = False
                            break
    except Exception:
        h1 = False

    neg_q = False
    try:
        if n_int == 0:
            phi_n = 0
        else:
            phi_n = sympy.totient(abs(n_int))
        
        if isinstance(zeta, (int, float)) or (isinstance(zeta, sympy.Expr) and zeta.is_Rational):
            deg = 1
        elif isinstance(zeta, sympy.Symbol):
            deg = float('inf')
        else:
            try:
                minpoly = sympy.minpoly(zeta)
                deg = sympy.degree(minpoly)
            except Exception:
                deg = float('inf')
            
        if deg != phi_n:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: zeta_n is a primitive n-th root of unity", "not_Q: The degree of the field extension is not equal to phi(n)"]
N_HYP = 1
NEG_Q_INDEX = 1