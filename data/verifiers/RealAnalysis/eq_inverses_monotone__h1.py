import itertools

def evaluate(func, val):
    try:
        return float(func(val))
    except TypeError:
        from sympy.abc import x
        return float(func.subs(x, val))

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    Order of return: [H1_ok, H2_ok, neg_Q_ok]
    """
    H1_ok = False
    H2_ok = False
    neg_Q_ok = False
    
    try:
        alpha = float(witness.alpha)
        a = float(witness.a)
        b = float(witness.b)
        
        if alpha > 0:
            H1_ok = True
            grid = [a + i * (b - a) / 50.0 for i in range(51)]
            for f in itertools.islice(witness.F, 100):
                for i in range(len(grid)):
                    for j in range(i + 1, len(grid)):
                        x_val = grid[i]
                        y_val = grid[j]
                        fx = evaluate(f, x_val)
                        fy = evaluate(f, y_val)
                        if fy - fx < alpha * (y_val - x_val) - 1e-5:
                            H1_ok = False
                            break
                    if not H1_ok:
                        break
                if not H1_ok:
                    break
    except Exception:
        H1_ok = False

    try:
        a = float(witness.a)
        b = float(witness.b)
        c = float(witness.c)
        d = float(witness.d)
        
        H2_ok = True
        grid = [c + i * (d - c) / 50.0 for i in range(51)]
        for f, f_inv in itertools.islice(zip(witness.F, witness.F_inv), 100):
            for u in grid:
                x_val = evaluate(f_inv, u)
                if not (a - 1e-5 <= x_val <= b + 1e-5):
                    H2_ok = False
                    break
                fx = evaluate(f, x_val)
                if abs(fx - u) > 1e-5:
                    H2_ok = False
                    break
            if not H2_ok:
                break
    except Exception:
        H2_ok = False

    try:
        if hasattr(witness, 'is_uniformly_equicontinuous'):
            if callable(witness.is_uniformly_equicontinuous):
                neg_Q_ok = not witness.is_uniformly_equicontinuous()
            else:
                neg_Q_ok = not witness.is_uniformly_equicontinuous
        elif hasattr(witness, 'neg_Q'):
            if callable(witness.neg_Q):
                neg_Q_ok = bool(witness.neg_Q())
            else:
                neg_Q_ok = bool(witness.neg_Q)
        else:
            c = float(witness.c)
            d = float(witness.d)
            grid = [c + i * (d - c) / 100.0 for i in range(101)]
            max_slopes = []
            for f_inv in itertools.islice(witness.F_inv, 50):
                max_slope = 0
                for i in range(len(grid) - 1):
                    u = grid[i]
                    v = grid[i+1]
                    fu = evaluate(f_inv, u)
                    fv = evaluate(f_inv, v)
                    slope = abs(fv - fu) / (v - u)
                    if slope > max_slope:
                        max_slope = slope
                max_slopes.append(max_slope)
                
            if len(max_slopes) > 1 and max(max_slopes) > 1000 and max_slopes[-1] > max_slopes[0] * 10:
                neg_Q_ok = True
            else:
                neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [H1_ok, H2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: There exists a constant alpha > 0 such that f(y) - f(x) >= alpha(y - x) for all f in F and x < y",
    "H_2: F_inv is the family of inverse functions",
    "¬Q: The family F_inv is not uniformly equicontinuous"
]

N_HYP = 2
NEG_Q_INDEX = 2