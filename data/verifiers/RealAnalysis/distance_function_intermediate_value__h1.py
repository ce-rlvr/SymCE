import sympy as sp
from sympy import eye, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(witness, attr):
    if isinstance(witness, dict):
        return witness[attr]
    return getattr(witness, attr)

def eval_gamma(gamma, t_val):
    if callable(gamma):
        res = gamma(t_val)
    else:
        t = sp.Symbol('t', real=True)
        res = gamma.subs(t, t_val)
    if not isinstance(res, sp.Matrix):
        res = sp.Matrix(res)
    return res

def get_min_d(pt, K):
    if hasattr(K, 'distance'):
        return float(K.distance(pt))
    elif isinstance(K, sp.Interval):
        pt_val = float(pt[0])
        start = float(K.start)
        end = float(K.end)
        if pt_val < start:
            return start - pt_val
        elif pt_val > end:
            return pt_val - end
        else:
            return 0.0
    else:
        return min(float((pt - sp.Matrix(j)).norm()) for j in K)

def conditions(witness):
    try:
        x = sp.Matrix(get_attr(witness, 'x'))
        y = sp.Matrix(get_attr(witness, 'y'))
        gamma = get_attr(witness, 'gamma')
        v = sp.sympify(get_attr(witness, 'v'))
        K = get_attr(witness, 'K')
    except Exception:
        return [False, False, False, False]

    # H1: x and y are points in R^n
    try:
        h1 = (x.shape == y.shape and x.shape[1] == 1)
    except Exception:
        h1 = False

    # H2: gamma is a continuous path such that gamma(0) = x and gamma(1) = y
    try:
        g0 = eval_gamma(gamma, 0)
        g1 = eval_gamma(gamma, 1)
        h2 = (float((g0 - x).norm()) < 1e-7 and float((g1 - y).norm()) < 1e-7)
    except Exception:
        h2 = False

    # H3: v is a real number that lies between inf ||x - k|| and inf ||y - k|| inclusive
    try:
        if not v.is_real:
            h3 = False
        else:
            dist_x = get_min_d(x, K)
            dist_y = get_min_d(y, K)
            min_val = min(dist_x, dist_y)
            max_val = max(dist_x, dist_y)
            h3 = bool(min_val - 1e-7 <= float(v) <= max_val + 1e-7)
    except Exception:
        h3 = False

    # Conclusion: exists t in [0, 1] such that inf ||gamma(t) - k|| == v
    try:
        conclusion_holds = False
        t = sp.Symbol('t', real=True)
        
        try:
            if callable(gamma):
                gamma_t = sp.Matrix(gamma(t))
            else:
                gamma_t = sp.Matrix(gamma)
        except Exception:
            gamma_t = None

        candidates = set()
        if gamma_t is not None:
            if hasattr(K, 'distance'):
                try:
                    eq = K.distance(gamma_t) - v
                    sols = sp.solve(eq, t)
                    for sol in sols:
                        try:
                            sol_f = float(sol)
                            if 0 <= sol_f <= 1:
                                candidates.add(sol_f)
                        except TypeError:
                            pass
                except Exception:
                    pass
            elif isinstance(K, sp.Interval):
                pass
            else:
                for k in K:
                    try:
                        k_mat = sp.Matrix(k)
                        eq = sp.simplify((gamma_t - k_mat).dot(gamma_t - k_mat) - v**2)
                        sols = sp.solve(eq, t)
                        for sol in sols:
                            try:
                                sol_f = float(sol)
                                if 0 <= sol_f <= 1:
                                    candidates.add(sol_f)
                            except TypeError:
                                pass
                    except Exception:
                        pass

        for sol in candidates:
            try:
                pt = eval_gamma(gamma, sol)
                min_d = get_min_d(pt, K)
                if abs(min_d - float(v)) < 1e-7:
                    conclusion_holds = True
                    break
            except Exception:
                pass

        if not conclusion_holds:
            for i in range(10001):
                try:
                    t_val = i / 10000.0
                    pt = eval_gamma(gamma, t_val)
                    min_d = get_min_d(pt, K)
                    if abs(min_d - float(v)) <= 1e-3:
                        conclusion_holds = True
                        break
                except Exception:
                    pass

        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are points in R^n",
    "H_2: gamma is a continuous path such that gamma(0) = x and gamma(1) = y",
    "H_3: v is a real number that lies between inf ||x - k|| and inf ||y - k|| inclusive",
    "¬Q: There does not exist t in the interval 0 to 1 such that inf ||gamma(t) - k|| = v"
]

N_HYP = 3
NEG_Q_INDEX = 3