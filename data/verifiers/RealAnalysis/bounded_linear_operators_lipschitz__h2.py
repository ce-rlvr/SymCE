import sympy as sp
import math
import itertools

# Top-level setup
x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: X and Y are normed vector spaces",
    "H_2: ||Tx||_Y <= M||x||_X for all x in X",
    "¬Q: T is not globally Lipschitz continuous with constant M"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                T, M = witness
            elif len(witness) >= 3:
                T = witness[0]
                M = witness[1]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
        M = float(M)
    except Exception:
        return [False, False, False]

    is_callable = callable(T)
    
    def get_evaluator(T, is_callable):
        if is_callable:
            return lambda p: float(T(p))
        else:
            try:
                T_func = sp.lambdify(x, T, modules=['math', 'sympy'])
                # Test evaluation on a few points to ensure lambdify succeeded
                float(T_func(1.0))
                float(T_func(-1.0))
                float(T_func(0.0))
                return lambda p: float(T_func(p))
            except Exception:
                return lambda p: float(T.subs(x, p).evalf())

    try:
        evaluator = get_evaluator(T, is_callable)
        # Test evaluation to ensure it's a valid scalar function on R
        v = evaluator(1.0)
        h1 = True
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]

    h2 = (M > 0)
    
    # Define a dense and sparse grid of points to check the conditions
    points = []
    for i in range(-1000, 1001):
        points.append(i / 100.0)  # -10.0 to 10.0 with step 0.01
    for i in range(-100, 101):
        if abs(i) > 10:
            points.append(i * 1.0)  # -100.0 to 100.0 with step 1.0
    for i in range(-100, 101):
        if abs(i) > 10:
            points.append(i * 10.0) # -1000.0 to 1000.0 with step 10.0
            
    T_vals = {}
    try:
        for p in points:
            val = evaluator(p)
            T_vals[p] = val
            if h2 and abs(val) > M * abs(p) + 1e-9:
                h2 = False
    except Exception:
        h2 = False

    neg_q = False
    try:
        sorted_points = sorted(T_vals.keys())
        if len(sorted_points) >= 2:
            # Check adjacent points (catches large local derivatives)
            for i in range(len(sorted_points) - 1):
                p1 = sorted_points[i]
                p2 = sorted_points[i+1]
                if abs(T_vals[p1] - T_vals[p2]) > M * abs(p1 - p2) + 1e-7:
                    neg_q = True
                    break
            
            if not neg_q:
                # Check all pairs in a subset (catches global Lipschitz violations)
                subset = sorted_points[::5]
                for p1, p2 in itertools.combinations(subset, 2):
                    if abs(T_vals[p1] - T_vals[p2]) > M * abs(p1 - p2) + 1e-7:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]