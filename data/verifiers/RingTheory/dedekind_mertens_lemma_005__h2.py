import sympy
from sympy import Poly, expand, groebner
import functools

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: c(f) and c(g) are the content ideals of f and g in R",
    "H_3: m is the degree of the polynomial g",
    "¬Q: c(f)^{m+1} c(g) != c(f)^m c(fg)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            g = witness['g']
            x = witness['x']
            I_gens = witness.get('I', [])
            vars_ = witness.get('vars', [])
        elif len(witness) == 3:
            f, g, x = witness
            I_gens = []
            vars_ = []
        elif len(witness) == 5:
            f, g, x, I_gens, vars_ = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        f_poly = Poly(f, x)
        g_poly = Poly(g, x)
        H1 = True
    except Exception:
        H1 = False

    try:
        c_f = f_poly.coeffs()
        c_g = g_poly.coeffs()
        H2 = True
    except Exception:
        H2 = False

    try:
        m = g_poly.degree()
        H3 = True
    except Exception:
        H3 = False

    try:
        if m < 0:
            m = 0
            
        if m > 20:
            return [H1, H2, H3, False]

        fg_poly = Poly(expand(f * g), x)
        c_fg = fg_poly.coeffs()

        def ideal_mul(A, B):
            return [expand(a * b) for a in A for b in B]

        def ideal_pow(A, n):
            if n == 0:
                return [1]
            res = A
            for _ in range(n - 1):
                res = ideal_mul(res, A)
            return res

        lhs = ideal_mul(ideal_pow(c_f, m + 1), c_g)
        rhs = ideal_mul(ideal_pow(c_f, m), c_fg)

        if not vars_:
            if any(expand(ig) != 0 for ig in I_gens):
                is_equal = True
            else:
                lhs_zero = all(expand(a) == 0 for a in lhs)
                rhs_zero = all(expand(a) == 0 for a in rhs)
                is_equal = (lhs_zero == rhs_zero)
        else:
            B_plus_I = rhs + I_gens
            A_plus_I = lhs + I_gens
            
            is_equal = True
            
            if B_plus_I:
                gb_B = groebner(B_plus_I, *vars_, domain='QQ')
                for a in lhs:
                    if gb_B.reduce(a)[1] != 0:
                        is_equal = False
                        break
            else:
                for a in lhs:
                    if expand(a) != 0:
                        is_equal = False
                        break
            
            if is_equal:
                if A_plus_I:
                    gb_A = groebner(A_plus_I, *vars_, domain='QQ')
                    for b in rhs:
                        if gb_A.reduce(b)[1] != 0:
                            is_equal = False
                            break
                else:
                    for b in rhs:
                        if expand(b) != 0:
                            is_equal = False
                            break

        neg_Q = not is_equal
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]