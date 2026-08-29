import sympy
from sympy import cyclotomic_poly, minpoly, simplify, I, pi, exp
from sympy.abc import x

# Top-level setup
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        n, zeta, poly = witness
    except Exception:
        return [False, False, False]

    # H1: zeta is a primitive n-th root of unity in C
    try:
        if not isinstance(n, (int, sympy.Integer)):
            h1_ok = False
        else:
            # Check zeta**n == 1
            is_root = simplify(zeta**n - 1) == 0
            # Check primitivity
            is_primitive = True
            if n > 0:
                for k in range(1, int(n)):
                    if simplify(zeta**k - 1) == 0:
                        is_primitive = False
                        break
            else:
                is_primitive = False
                
            h1_ok = bool(is_root and is_primitive)
    except Exception:
        h1_ok = False

    # H2: poly is the n-th cyclotomic polynomial
    try:
        expected_poly = cyclotomic_poly(int(n), x)
        h2_ok = bool(simplify(poly - expected_poly) == 0)
    except Exception:
        h2_ok = False

    # neg_Q: poly is NOT the minimal polynomial of zeta over Q
    try:
        actual_minpoly = minpoly(zeta, x)
        neg_q_ok = bool(simplify(poly - actual_minpoly) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity",
    "H_2: Phi_n is the n-th cyclotomic polynomial",
    "not Q: Phi_n is NOT the minimal polynomial of zeta_n over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2