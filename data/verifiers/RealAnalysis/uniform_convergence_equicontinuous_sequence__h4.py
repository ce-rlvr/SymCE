import sympy as sp
from sympy import Interval, FiniteSet, Union, oo, S

# Top-level setup
x, n = sp.symbols('x n')

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness.get('K'), witness.get('f_n'), witness.get('x'), witness.get('n')
    elif isinstance(witness, (list, tuple)) and len(witness) == 4:
        return witness[0], witness[1], witness[2], witness[3]
    return None, None, None, None

def conditions(witness) -> list[bool]:
    K, f_n, w_x, w_n = parse_witness(witness)
    if K is None or f_n is None or w_x is None or w_n is None:
        return [False, False, False, False]
    
    # H1: K is a compact metric space
    try:
        def is_compact(K_set):
            if isinstance(K_set, sp.Interval):
                return not K_set.left_open and not K_set.right_open and K_set.measure < sp.oo
            if isinstance(K_set, sp.FiniteSet):
                return True
            if isinstance(K_set, sp.Union):
                return all(is_compact(arg) for arg in K_set.args)
            return False
        h1 = is_compact(K)
    except Exception:
        h1 = False

    # H2: f_n is a sequence of continuous real-valued functions on K
    try:
        from sympy.calculus.util import continuous_domain
        h2 = True
        if isinstance(K, sp.Interval):
            a = float(K.start)
            b = float(K.end)
            points = [a + (b - a) * i / 20.0 for i in range(21)]
            points += [a + (b - a) * ((i * 137) % 1000) / 1000.0 for i in range(20)]
        elif isinstance(K, sp.FiniteSet):
            points = [float(p) for p in K.args]
        else:
            points = None
            h2 = False
            
        if points is not None:
            for i in [1, 2, 3]:
                f_i = f_n.subs(w_n, i)
                for p in points:
                    val = f_i.subs(w_x, p).evalf()
                    if not val.is_real or not val.is_finite:
                        h2 = False
                        break
                if not h2:
                    break
                if isinstance(K, sp.Interval):
                    try:
                        dom = continuous_domain(f_i, w_x, S.Reals)
                        if not K.is_subset(dom):
                            h2 = False
                    except Exception:
                        pass
    except Exception:
        h2 = False

    # H3: f_n is equicontinuous on K
    try:
        h3 = True
        if isinstance(K, sp.Interval):
            a = float(K.start)
            b = float(K.end)
            delta = 1e-5
            points = [a + (b - a) * i / 100.0 for i in range(101)]
            points += [a + (b - a) * ((i * 137) % 1000) / 1000.0 for i in range(100)]
            
            for x0 in points:
                for sign in [-1, 1]:
                    x1 = x0 + sign * delta
                    if x1 < a or x1 > b:
                        continue
                    
                    for i in [1, 10, 100, 1000, 10000, 100000]:
                        val0 = f_n.subs({w_x: x0, w_n: i}).evalf()
                        val1 = f_n.subs({w_x: x1, w_n: i}).evalf()
                        if abs(val0 - val1) > 0.1:
                            h3 = False
                            break
                    if not h3:
                        break
                if not h3:
                    break
        elif isinstance(K, sp.FiniteSet):
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: f_n does not converge uniformly on K
    try:
        neg_q = False
        if isinstance(K, sp.Interval):
            a = float(K.start)
            b = float(K.end)
            points = [a + (b - a) * i / 100.0 for i in range(101)]
            points += [a + (b - a) * ((i * 137) % 1000) / 1000.0 for i in range(100)]
        elif isinstance(K, sp.FiniteSet):
            points = [float(p) for p in K.args]
        else:
            points = None
            neg_q = False
            
        if points is not None:
            for m in [1001, 1010, 2000, 10000]:
                max_diff = 0
                for x0 in points:
                    val_n = f_n.subs({w_x: x0, w_n: 1000}).evalf()
                    val_m = f_n.subs({w_x: x0, w_n: m}).evalf()
                    diff = abs(val_n - val_m)
                    if diff > max_diff:
                        max_diff = diff
                if max_diff > 0.1:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a compact metric space",
    "H_2: {f_n} is a sequence of continuous real-valued functions on K",
    "H_3: {f_n} is equicontinuous on K",
    "¬Q: {f_n} does not converge uniformly on K"
]

N_HYP = 3
NEG_Q_INDEX = 3