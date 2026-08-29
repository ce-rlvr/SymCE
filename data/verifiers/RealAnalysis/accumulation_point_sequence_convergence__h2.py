import sympy
import math

def evaluate_seq(seq, n):
    if callable(seq):
        return seq(n)
    elif isinstance(seq, (list, tuple)):
        return seq[n % len(seq)]
    elif hasattr(seq, 'subs'):
        syms = list(seq.free_symbols)
        if len(syms) == 1:
            return seq.subs(syms[0], n).evalf()
        else:
            n_sym = sympy.Symbol('n')
            return seq.subs(n_sym, n).evalf()
    raise ValueError("Unknown sequence format")

def get_unique_vals(seq, max_n):
    vals = []
    for n in range(1, max_n + 1):
        try:
            v = float(evaluate_seq(seq, n))
            vals.append(v)
        except Exception:
            pass
    return list(set(vals))

def count_near(u, unique_vals, eps=0.1):
    return sum(1 for v in unique_vals if 0 < abs(v - u) < eps)

def conditions(witness):
    try:
        X, seq, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: X is a compact metric space
    h1 = False
    try:
        if isinstance(X, sympy.Interval):
            h1 = (not X.left_open) and (not X.right_open) and X.inf.is_finite and X.sup.is_finite
        elif isinstance(X, sympy.FiniteSet):
            h1 = True
        elif hasattr(X, 'is_compact') and X.is_compact:
            h1 = True
        elif isinstance(X, set):
            h1 = True
        elif isinstance(X, (list, tuple)) and len(X) == 2:
            a, b = float(X[0]), float(X[1])
            h1 = math.isfinite(a) and math.isfinite(b)
    except Exception:
        pass

    # H2: The sequence has exactly one accumulation point x in X
    h2 = False
    try:
        unique_1000 = get_unique_vals(seq, 1000)
        unique_5000 = get_unique_vals(seq, 5000)
        
        c1_x = count_near(float(x), unique_1000, eps=0.1)
        c5_x = count_near(float(x), unique_5000, eps=0.1)
        
        if c5_x > c1_x and c5_x >= 10:
            other_acc = False
            for u in unique_5000:
                if abs(u - float(x)) > 0.2:
                    c1_u = count_near(u, unique_1000, eps=0.1)
                    c5_u = count_near(u, unique_5000, eps=0.1)
                    if c5_u > c1_u and c5_u >= 10:
                        other_acc = True
                        break
            h2 = not other_acc
    except Exception:
        pass

    # NegQ: The sequence does not converge to x
    neg_q = False
    try:
        blocks = []
        for start in [1000, 2000, 3000, 4000, 5000]:
            max_dist = 0
            for i in range(start, start + 20):
                val = evaluate_seq(seq, i)
                d = abs(float(val) - float(x))
                if d > max_dist:
                    max_dist = d
            blocks.append(max_dist)
            
        converges = False
        if blocks and blocks[-1] < 1e-2:
            converges = True
        elif len(blocks) == 5 and all(blocks[i] > blocks[i+1] for i in range(4)):
            converges = True
            
        neg_q = not converges
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: The sequence (x_n) has exactly one accumulation point x in X",
    "¬Q: The sequence (x_n) does not converge to x"
]

N_HYP = 2
NEG_Q_INDEX = 2