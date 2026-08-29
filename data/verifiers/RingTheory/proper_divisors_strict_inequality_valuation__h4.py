import sympy
from sympy.abc import x
from sympy import div

# Top-level setup
# The witness is expected to be of the form (R_name, d_func, a, b)
# where R_name is 'ZZ' or 'QQ[x]'.

def conditions(witness) -> list[bool]:
    def is_nonneg_int(val):
        try:
            if int(val) == val and val >= 0:
                return True
        except Exception:
            pass
        return False

    try:
        R, d, a, b = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: R is a Euclidean domain
    try:
        h1 = R in ['ZZ', 'QQ[x]']
    except Exception:
        h1 = False
        
    # H2: d is a submultiplicative Euclidean function on R
    try:
        h2 = False
        if h1:
            if R == 'ZZ':
                elements = [1, -1, 2, -2, 3, 5, 6, 10]
                zero = 0
            elif R == 'QQ[x]':
                elements = [sympy.Integer(1), sympy.Integer(-2), x, x+1, x**2, 2*x, x**2+x+1, x**3]
                zero = sympy.Integer(0)
            
            h2_ok = True
            for e in elements:
                if not is_nonneg_int(d(e)):
                    h2_ok = False
                    break
            
            if h2_ok:
                for e1 in elements:
                    for e2 in elements:
                        if d(e1*e2) > d(e1)*d(e2):
                            h2_ok = False
                            break
                        if R == 'ZZ':
                            q_base = e1 // e2
                            found = False
                            for q_cand in (q_base, q_base+1, q_base-1):
                                r_cand = e1 - q_cand * e2
                                if r_cand == zero or d(r_cand) < d(e2):
                                    found = True
                                    break
                            if not found:
                                h2_ok = False
                                break
                        elif R == 'QQ[x]':
                            q, r = div(e1, e2, domain='QQ')
                            if r != zero and d(r) >= d(e2):
                                h2_ok = False
                                break
                    if not h2_ok:
                        break
            h2 = h2_ok
    except Exception:
        h2 = False

    # H3: a and b are non-zero elements of R
    try:
        if R == 'ZZ':
            h3 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and a != 0 and b != 0
        elif R == 'QQ[x]':
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
            a_poly = sympy.poly(a_expr, x, domain='QQ')
            b_poly = sympy.poly(b_expr, x, domain='QQ')
            h3 = not a_poly.is_zero and not b_poly.is_zero
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: d(a) == d(b)
    try:
        h4 = d(a) == d(b)
    except Exception:
        h4 = False

    # Conclusion: a and b are associate elements in R
    try:
        if R == 'ZZ':
            assoc = (a % b == 0) and (b % a == 0)
        elif R == 'QQ[x]':
            a_expr = sympy.sympify(a)
            b_expr = sympy.sympify(b)
            q1, r1 = div(a_expr, b_expr, domain='QQ')
            q2, r2 = div(b_expr, a_expr, domain='QQ')
            assoc = (r1 == 0) and (r2 == 0)
        else:
            assoc = True
        neg_q = not assoc
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: d is a submultiplicative Euclidean function on R",
    "H_3: a and b are non-zero elements of R",
    "H_4: d(a) = d(b)",
    "¬Q: a and b are not associate elements in R"
]

N_HYP = 4
NEG_Q_INDEX = 4