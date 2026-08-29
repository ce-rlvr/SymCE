import sympy as sp
import math

# Top-level setup
n, x = sp.symbols('n x', real=True)

def get_sample_points(X):
    if hasattr(X, 'is_Interval') and X.is_Interval:
        start = -10.0 if X.start == sp.S.NegativeInfinity else float(X.start)
        end = 10.0 if X.end == sp.S.Infinity else float(X.end)
        # Sample strictly inside to avoid boundary singularities
        return [start + (end - start) * i / 20.0 for i in range(1, 20)]
    elif hasattr(X, '__iter__'):
        return list(X)
    else:
        return [float(X)]

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        return witness[0], get_sample_points(witness[1])
    else:
        # Default to a single point domain if not specified
        return witness, [0.0]

def eval_f(f, n_val, x_val):
    if hasattr(f, 'subs'):
        val = f.subs({n: n_val, x: x_val})
        return float(val)
    else:
        val = f(n_val, x_val)
        return float(val)

def check_h1(witness):
    try:
        f, pts = parse_witness(witness)
        if not pts:
            return False
        for n_val in range(1, 6):
            for x_val in pts:
                val = eval_f(f, n_val, x_val)
                if not math.isfinite(val):
                    return False
        return True
    except Exception:
        return False

def check_h2(witness):
    try:
        f, pts = parse_witness(witness)
        if not pts:
            return False
        for n_val in range(1, 6):
            vals = [abs(eval_f(f, n_val, x_val)) for x_val in pts]
            if not all(math.isfinite(v) for v in vals):
                return False
        return True
    except Exception:
        return False

def check_neg_q(witness):
    try:
        f, pts = parse_witness(witness)
        if not pts:
            return False
        max_vals = []
        for n_val in [1, 10, 100, 1000, 10000]:
            vals = [abs(eval_f(f, n_val, x_val)) for x_val in pts]
            max_vals.append(max(vals))
        
        # Check if the supremum over x grows without bound as n increases
        if max(max_vals) > 1000:
            return True
            
        if max_vals[-1] > max_vals[0] and max_vals[-1] > 100:
            return True
            
        return False
    except Exception:
        return False

def conditions(witness):
    return [check_h1(witness), check_h2(witness), check_neg_q(witness)]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions defined on a set X",
    "H_2: Each function f_n is bounded on X",
    "¬Q: The sequence (f_n) is not uniformly bounded on X"
]

N_HYP = 2
NEG_Q_INDEX = 2