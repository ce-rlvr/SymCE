import math
import itertools
import sympy as sp

# Top-level setup
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True)

def get_points(S):
    num_points = 50
    if isinstance(S, tuple) and len(S) == 2:
        a, b = float(S[0]), float(S[1])
        return [a + (b - a) * i / num_points for i in range(num_points + 1)]
    elif hasattr(S, 'is_Interval') and S.is_Interval:
        a = float(S.start) if str(S.start) != '-oo' else -10.0
        b = float(S.end) if str(S.end) != 'oo' else 10.0
        return [a + (b - a) * i / num_points for i in range(num_points + 1)]
    elif str(S) == 'Reals':
        a, b = -10.0, 10.0
        return [a + (b - a) * i / num_points for i in range(num_points + 1)]
    elif hasattr(S, '__iter__'):
        return list(S)
    else:
        return []

def get_distance(witness, u, v):
    if 'd' in witness:
        return float(witness['d'](u, v))
    try:
        return float(abs(u - v))
    except Exception:
        return math.sqrt(sum((float(a) - float(b))**2 for a, b in zip(u, v)))

def conditions(witness):
    try:
        S = witness['S']
        f_n = witness['f_n']
        f = witness['f']
        L = float(witness['L'])
        points = get_points(S)
        if 'extra_points' in witness:
            points.extend(witness['extra_points'])
        if not points:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: {f_n} is a sequence of functions from S to R
    h1 = False
    try:
        h1_ok = True
        for pt in points[:5]:
            val = f_n(1, pt)
            try:
                float(val)
            except Exception:
                h1_ok = False
                break
        h1 = h1_ok
    except Exception:
        h1 = False

    # H2: f_n is L-Lipschitz on S for all n
    h2 = False
    try:
        h2_ok = True
        for n_val in range(1, 20):
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    u = points[i]
                    v = points[j]
                    dist = get_distance(witness, u, v)
                    if dist > 1e-9:
                        val_u = float(f_n(n_val, u))
                        val_v = float(f_n(n_val, v))
                        if abs(val_u - val_v) > L * dist + 1e-5:
                            h2_ok = False
                            break
                if not h2_ok:
                    break
            if not h2_ok:
                break
        h2 = h2_ok
    except Exception:
        h2 = False

    # H3: {f_n} converges uniformly to f on S
    h3 = False
    try:
        h3_ok = True
        diffs = []
        for n_val in [10, 100, 1000, 10000]:
            max_diff = 0
            for pt in points:
                diff = abs(float(f_n(n_val, pt)) - float(f(pt)))
                if diff > max_diff:
                    max_diff = diff
            diffs.append(max_diff)
        if diffs[-1] > 0.5:
            h3_ok = False
        if len(diffs) > 1 and diffs[-1] > diffs[0] and diffs[-1] > 1e-5:
            h3_ok = False
        h3 = h3_ok
    except Exception:
        h3 = False

    # neg_Q: f is NOT L-Lipschitz on S
    neg_q = False
    try:
        neg_q_ok = False
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                u = points[i]
                v = points[j]
                dist = get_distance(witness, u, v)
                if dist > 1e-9:
                    if abs(float(f(u)) - float(f(v))) > L * dist + 1e-5:
                        neg_q_ok = True
                        break
            if neg_q_ok:
                break
        neg_q = neg_q_ok
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of functions from S to R",
    "H_2: f_n is Lipschitz continuous on S with constant L for all n",
    "H_3: {f_n} converges uniformly to f on S",
    "¬Q: f is not Lipschitz continuous on S with constant L"
]

N_HYP = 3
NEG_Q_INDEX = 3