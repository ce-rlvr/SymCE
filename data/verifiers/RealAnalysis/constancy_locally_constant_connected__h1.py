import sympy
from sympy import oo

# Top-level setup
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: Y is a topological space",
    "H_2: f: X \\to Y is a locally constant function",
    "¬Q: f is not a constant function on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        X = witness['X']
        f = witness['f']
    except (TypeError, KeyError, Exception):
        return [False, False, False]
    
    # H_1: Y is a topological space
    # The codomain of f is implicitly a subset of C or R, which are topological spaces.
    h1_ok = True
    
    def sample_points(S):
        points = set()
        t_name = type(S).__name__
        if t_name == 'Union':
            for arg in S.args:
                points.update(sample_points(arg))
        elif t_name == 'Interval':
            a, b = S.start, S.end
            if a == -oo and b == oo:
                points.update([-10.0, 0.0, 10.0])
            elif a == -oo:
                b_f = float(b)
                points.update([b_f-10.0, b_f-1.0, b_f-0.1])
            elif b == oo:
                a_f = float(a)
                points.update([a_f+0.1, a_f+1.0, a_f+10.0])
            else:
                a_f = float(a)
                b_f = float(b)
                points.update([a_f + 0.1*(b_f-a_f), a_f + 0.5*(b_f-a_f), a_f + 0.9*(b_f-a_f)])
                if not S.left_open: points.add(a_f)
                if not S.right_open: points.add(b_f)
        elif t_name == 'FiniteSet':
            for p in S.args:
                points.add(float(p))
        elif S == sympy.S.Reals or t_name == 'Reals':
            points.update([-10.0, 0.0, 10.0])
        elif isinstance(S, (list, tuple, set)):
            for arg in S:
                points.update(sample_points(arg))
        return list(points)

    def eval_f(func, p):
        if isinstance(func, dict):
            v = func.get(p, func.get(float(p)))
            if v is None:
                raise ValueError("Point not in dict")
        elif callable(func):
            v = func(p)
        elif hasattr(func, 'free_symbols'):
            free = list(func.free_symbols)
            if not free:
                v = func
            else:
                v = func.subs(free[0], p)
        else:
            v = func
        return complex(v)

    # H_2: f is locally constant on X
    try:
        if hasattr(X, 'args') and type(X).__name__ == 'Union':
            components = X.args
        elif isinstance(X, (list, tuple, set)):
            components = X
        else:
            components = [X]
            
        locally_constant = True
        all_pts = []
        for comp in components:
            pts = sample_points(comp)
            if not pts:
                continue
            all_pts.extend(pts)
            vals = [eval_f(f, p) for p in pts]
            if any(abs(v - vals[0]) > 1e-7 for v in vals):
                locally_constant = False
                break
        h2_ok = locally_constant and len(all_pts) > 0
    except Exception:
        h2_ok = False
        all_pts = []

    # ¬Q: f is not a constant function on X
    try:
        neg_q_ok = False
        if all_pts:
            vals = [eval_f(f, p) for p in all_pts]
            if any(abs(v - vals[0]) > 1e-7 for v in vals):
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]