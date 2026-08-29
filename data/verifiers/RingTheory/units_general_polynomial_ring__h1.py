import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        f_coeffs, g_coeffs = witness
    except Exception:
        return [False, False, False]

    def is_zero(A):
        try:
            if hasattr(A, 'shape'):
                for i in range(A.shape[0]):
                    for j in range(A.shape[1]):
                        if sympy.simplify(A[i, j]) != 0:
                            return False
                return True
            else:
                return sympy.simplify(A) == 0
        except Exception:
            return False

    def get_zero_and_one(coeffs):
        for c in coeffs:
            if hasattr(c, 'shape'):
                return sympy.zeros(*c.shape), sympy.eye(c.shape[0])
        return 0, 1

    try:
        zero, one = get_zero_and_one(f_coeffs + g_coeffs)
    except Exception:
        return [False, False, False]

    def poly_mul(coeffs1, coeffs2):
        if not coeffs1 or not coeffs2:
            return []
        deg1 = len(coeffs1) - 1
        deg2 = len(coeffs2) - 1
        res = [zero] * (deg1 + deg2 + 1)
        for i in range(deg1 + 1):
            for j in range(deg2 + 1):
                term = coeffs1[i] * coeffs2[j]
                if res[i+j] is zero:
                    res[i+j] = term
                else:
                    res[i+j] = res[i+j] + term
        return res

    def is_one_poly(p):
        if not p: return False
        if not is_zero(p[0] - one): return False
        for c in p[1:]:
            if not is_zero(c): return False
        return True

    try:
        h1 = isinstance(f_coeffs, list) and len(f_coeffs) > 0
    except Exception:
        h1 = False

    try:
        fg = poly_mul(f_coeffs, g_coeffs)
        gf = poly_mul(g_coeffs, f_coeffs)
        h2 = is_one_poly(fg) and is_one_poly(gf)
    except Exception:
        h2 = False

    try:
        a0 = f_coeffs[0]
        b0 = g_coeffs[0]
        a0_is_unit = is_zero(a0 * b0 - one) and is_zero(b0 * a0 - one)
        
        def is_nilpotent(A):
            if hasattr(A, 'shape'):
                m = A.shape[0]
                return is_zero(A**m)
            else:
                return is_zero(A)
                
        all_nilpotent = True
        for a in f_coeffs[1:]:
            if not is_nilpotent(a):
                all_nilpotent = False
                break
                
        conclusion = a0_is_unit and all_nilpotent
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: f is a polynomial", "H_2: f is a unit", "not Q: a0 is not a unit or higher coeffs are not nilpotent"]

N_HYP = 2
NEG_Q_INDEX = 2