import sympy
import math
import random

# Top-level setup for the witness expression namespace
x, y, z = sympy.symbols('x y z', real=True)

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture:
    Hypothesis: f is Lipschitz continuous with constant L.
    Conclusion: Mf is Lipschitz continuous with constant L.
    """
    try:
        # Witness should be a tuple (f, L)
        f, L = witness
        L = float(L)
    except Exception:
        return [False, False]
        
    # Handle the case where f is provided as a callable rather than a sympy expression
    if callable(f):
        try:
            f = f(x)
        except Exception:
            pass

    try:
        free_syms = list(f.free_symbols)
    except Exception:
        free_syms = []
    if not free_syms:
        free_syms = [x]

    def check_h1():
        random.seed(42)
        # 1. Check Lipschitz condition via random sampling
        for _ in range(200):
            pt_a = [random.uniform(-100, 100) for _ in free_syms]
            pt_b = [random.uniform(-100, 100) for _ in free_syms]
            dist = math.sqrt(sum((a - b)**2 for a, b in zip(pt_a, pt_b)))
            if dist == 0: 
                continue
            try:
                subs_a = {sym: val for sym, val in zip(free_syms, pt_a)}
                subs_b = {sym: val for sym, val in zip(free_syms, pt_b)}
                val_a = float(f.subs(subs_a))
                val_b = float(f.subs(subs_b))
                if abs(val_a - val_b) > L * dist + 1e-5:
                    return False
            except Exception:
                return False
                
        # 2. Check partial derivatives if differentiable
        try:
            for sym in free_syms:
                df = f.diff(sym)
                for _ in range(50):
                    pt = [random.uniform(-100, 100) for _ in free_syms]
                    subs_dict = {s: val for s, val in zip(free_syms, pt)}
                    df_val = float(df.subs(subs_dict))
                    if abs(df_val) > L + 1e-5:
                        return False
        except Exception:
            pass
            
        return True

    try:
        h1_ok = check_h1()
    except Exception:
        h1_ok = False

    def check_neg_q():
        # If f is Lipschitz, Mf is Lipschitz with the same constant UNLESS Mf is identically infinity.
        # We check if Mf(0) = infinity by verifying if the average of |f| over large balls grows unboundedly.
        def eval_f_ray(t):
            subs_dict = {sym: t for sym in free_syms}
            return abs(float(f.subs(subs_dict)))

        def avg_abs_f(c, d):
            steps = 200
            dx = (d - c) / steps
            total = 0.0
            for i in range(steps):
                t_val = c + (i + 0.5) * dx
                total += eval_f_ray(t_val)
            return total / steps
            
        try:
            avg1 = avg_abs_f(-100, 100)
            avg2 = avg_abs_f(-1000, 1000)
            avg3 = avg_abs_f(-10000, 10000)
            
            # If the average grows significantly as the radius increases, Mf is infinity.
            if avg3 > 1.5 * avg2 and avg2 > 1.5 * avg1 and avg3 > 1e-5:
                return True
        except Exception:
            pass
            
        return False

    try:
        neg_q_ok = check_neg_q()
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous with constant L",
    "¬Q: Mf is not Lipschitz continuous with constant L"
]

N_HYP = 1
NEG_Q_INDEX = 1