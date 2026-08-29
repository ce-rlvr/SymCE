import math
import sympy as sp
from sympy import Symbol, Rational, exp, sin, cos, pi

# Top-level setup for witness expressions
x = Symbol('x')
n = Symbol('n')

CONDITION_LABELS = [
    "H_1: S is a symmetric set",
    "H_2: f_n is a sequence of real-valued functions defined on S",
    "H_3: E_n is the even part of f_n",
    "¬Q: E_n does not converge uniformly to E on S"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_val_2(f_obj, n_val, x_val):
    if isinstance(f_obj, (int, float)):
        return float(f_obj)
    if isinstance(f_obj, str):
        f_obj = sp.sympify(f_obj)
    if callable(f_obj):
        return float(f_obj(n_val, x_val))
    else:
        n_sym = sp.Symbol('n')
        x_sym = sp.Symbol('x')
        return float(f_obj.subs({n_sym: n_val, x_sym: x_val}))

def get_val_1(f_obj, x_val):
    if isinstance(f_obj, (int, float)):
        return float(f_obj)
    if isinstance(f_obj, str):
        f_obj = sp.sympify(f_obj)
    if callable(f_obj):
        return float(f_obj(x_val))
    else:
        x_sym = sp.Symbol('x')
        return float(f_obj.subs({x_sym: x_val}))

def conditions(witness):
    # H1: S is a symmetric set
    h1 = False
    test_pts = []
    try:
        S = witness["S"]
        if isinstance(S, tuple) and len(S) == 2:
            if math.isinf(float(S[0])) or math.isinf(float(S[1])):
                h1 = (float(S[0]) == -float(S[1]))
                test_pts = [-100.0 + i*200.0/1000 for i in range(1001)]
            else:
                h1 = math.isclose(float(S[0]), float(-S[1]))
                test_pts = [float(S[0]) + i*(float(S[1])-float(S[0]))/1000 for i in range(1001)]
        elif hasattr(S, 'inf') and hasattr(S, 'sup'):
            if math.isinf(float(S.inf)) or math.isinf(float(S.sup)):
                h1 = (float(S.inf) == -float(S.sup))
                test_pts = [-100.0 + i*200.0/1000 for i in range(1001)]
            else:
                h1 = math.isclose(float(S.inf), float(-S.sup))
                test_pts = [float(S.inf) + i*(float(S.sup)-float(S.inf))/1000 for i in range(1001)]
        else:
            S_list = list(S)
            h1 = all(any(math.isclose(float(-pt), float(y)) for y in S_list) for pt in S_list)
            test_pts = [float(pt) for pt in S_list]
    except Exception:
        h1 = False

    # H2: f_n is a sequence of real-valued functions defined on S
    h2 = False
    try:
        if not test_pts:
            h2 = False
        else:
            f_n = witness["f_n"]
            h2 = True
            for n_val in [1, 2, 3]:
                for x_val in [test_pts[0], test_pts[len(test_pts)//2], test_pts[-1]]:
                    val = get_val_2(f_n, n_val, x_val)
                    if math.isnan(val) or math.isinf(val):
                        h2 = False
    except Exception:
        h2 = False

    # H3: E_n is the even part of f_n
    h3 = False
    try:
        if not test_pts:
            h3 = False
        elif "E_n" in witness:
            E_n_wit = witness["E_n"]
            f_n = witness["f_n"]
            h3 = True
            for n_val in [1, 2]:
                for x_val in [test_pts[0], test_pts[len(test_pts)//2], test_pts[-1]]:
                    expected = (get_val_2(f_n, n_val, x_val) + get_val_2(f_n, n_val, -x_val)) / 2.0
                    actual = get_val_2(E_n_wit, n_val, x_val)
                    if not math.isclose(actual, expected, abs_tol=1e-5):
                        h3 = False
        else:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: E_n does not converge uniformly to E on S
    neg_q = False
    try:
        if "f" not in witness or "f_n" not in witness or not test_pts:
            pass
        else:
            f = witness["f"]
            f_n = witness["f_n"]
            
            def E_n(n_val, x_val):
                return (get_val_2(f_n, n_val, x_val) + get_val_2(f_n, n_val, -x_val)) / 2.0
                
            def E(x_val):
                return (get_val_1(f, x_val) + get_val_1(f, -x_val)) / 2.0
                
            errors = []
            for n_val in [10, 100, 1000, 10000]:
                max_err = 0
                for pt in test_pts:
                    try:
                        val_En = E_n(n_val, pt)
                        val_E = E(pt)
                        err = abs(val_En - val_E)
                        if err > max_err:
                            max_err = err
                    except Exception:
                        max_err = float('inf')
                errors.append(max_err)
                
            if math.isnan(errors[-1]):
                neg_q = True
            elif errors[-1] > 1e-5 and errors[-1] >= errors[-2] * 0.8:
                neg_q = True
            elif errors[-1] > 0.1:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]