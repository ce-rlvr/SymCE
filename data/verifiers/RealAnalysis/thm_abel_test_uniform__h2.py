import sympy
from sympy import Symbol, Sum, oo, Abs, limit, Interval
import math
import itertools
import functools

# Top-level setup
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def get_points(D):
    points = []
    if isinstance(D, tuple) and len(D) == 2:
        try:
            a, b = float(D[0]), float(D[1])
            points = [a + (b - a) * i / 20.0 for i in range(1, 20)]
            return points
        except Exception:
            pass
    if hasattr(D, 'boundary'):
        try:
            if D.is_Interval:
                a = float(D.start) if D.start.is_finite else -10.0
                b = float(D.end) if D.end.is_finite else 10.0
                for i in range(1, 20):
                    points.append(a + (b - a) * i / 20.0)
                points.append(a + 1e-5)
                points.append(b - 1e-5)
                return points
        except Exception:
            pass
    if hasattr(D, '__iter__'):
        try:
            points = list(D)[:20]
            if points: return points
        except Exception:
            pass
    return [i/20.0 for i in range(1, 20)]

def check_uniform_convergence(term_func, points):
    N_max = 100
    S = {xv: [] for xv in points}
    for xv in points:
        current_sum = 0
        for nv in range(1, N_max + 1):
            try:
                current_sum += term_func(nv, xv)
            except Exception:
                pass
            S[xv].append(current_sum)
            
    max_diffs = []
    for N in range(75, N_max):
        diffs = []
        for xv in points:
            try:
                diffs.append(abs(S[xv][-1] - S[xv][N]))
            except Exception:
                diffs.append(float('inf'))
        max_diffs.append(max(diffs))
        
    if not max_diffs:
        return False
    return max(max_diffs) < 1e-2

def conditions(witness):
    try:
        if hasattr(witness, 'D') and hasattr(witness, 'f'):
            D = witness.D
            f = witness.f
            g = witness.g
            M = witness.M
        elif isinstance(witness, dict):
            D = witness.get('D', [0.5])
            f = witness.get('f')
            g = witness.get('g')
            M = witness.get('M', 1.0)
        else:
            D, f, g, M = witness
    except Exception:
        return [False, False, False, False, False]

    def eval_f(nv, xv):
        if callable(f): return float(f(nv, xv))
        subs_dict = {sym: (nv if sym.name == 'n' else xv) for sym in getattr(f, 'free_symbols', [])}
        return float(f.subs(subs_dict))

    def eval_g(nv, xv):
        if callable(g): return float(g(nv, xv))
        subs_dict = {sym: (nv if sym.name == 'n' else xv) for sym in getattr(g, 'free_symbols', [])}
        return float(g.subs(subs_dict))

    points = get_points(D)
    if not points:
        points = [0.5]

    # H1: D is a set
    try:
        h1 = hasattr(D, '__contains__') or hasattr(D, 'boundary') or isinstance(D, (list, set, tuple))
    except Exception:
        h1 = False

    # H2: sum f_n(x) converges uniformly on D
    try:
        h2 = check_uniform_convergence(eval_f, points)
    except Exception:
        h2 = False

    # H3: For each x in D, the sequence of real numbers (g_n(x)) is monotonic
    try:
        h3 = True
        for xv in points:
            diffs = []
            for nv in range(1, 20):
                try:
                    diffs.append(eval_g(nv+1, xv) - eval_g(nv, xv))
                except Exception:
                    pass
            if not diffs:
                continue
            is_inc = all(d >= -1e-7 for d in diffs)
            is_dec = all(d <= 1e-7 for d in diffs)
            if not (is_inc or is_dec):
                h3 = False
                break
    except Exception:
        h3 = False

    # H4: There exists a real number M > 0 such that |g_n(x)| <= M
    try:
        h4 = True
        M_val = float(M)
        for xv in points:
            for nv in range(1, 20):
                try:
                    if abs(eval_g(nv, xv)) > M_val + 1e-7:
                        h4 = False
                        break
                except Exception:
                    pass
            if not h4:
                break
    except Exception:
        h4 = False

    # neg_Q: The series sum f_n(x) g_n(x) does NOT converge uniformly on D
    try:
        def eval_fg(nv, xv):
            return eval_f(nv, xv) * eval_g(nv, xv)
        q = check_uniform_convergence(eval_fg, points)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: D is a set",
    "H_2: The series sum f_n(x) converges uniformly on D",
    "H_3: For each x in D, the sequence g_n(x) is monotonic",
    "H_4: There exists M > 0 such that |g_n(x)| <= M",
    "¬Q: The series sum f_n(x) g_n(x) does not converge uniformly on D"
]

N_HYP = 4
NEG_Q_INDEX = 4