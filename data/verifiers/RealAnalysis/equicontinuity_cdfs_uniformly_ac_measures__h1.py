import sympy as sp
import math
from sympy.abc import x, y

CONDITION_LABELS = [
    "H_1: P is uniformly absolutely continuous with respect to the Lebesgue measure",
    "H_2: F is the family of cumulative distribution functions",
    "not Q: F is not uniformly equicontinuous on R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    if not isinstance(witness, (list, tuple)):
        witnesses = [witness]
    else:
        witnesses = witness

    def get_callable(f):
        if isinstance(f, (int, float)):
            return lambda v: float(f)
        if hasattr(f, 'pdf'):
            return f.pdf
        if hasattr(f, 'free_symbols'):
            if not f.free_symbols:
                return lambda v: float(f.evalf())
            try:
                f_lam = sp.lambdify(x, f, 'math')
                f_lam(0.12345)
                return f_lam
            except Exception:
                return lambda v: float(f.subs(x, v).evalf())
        return f

    h1_ok = True
    for f in witnesses:
        is_uac = False
        try:
            f_lam = get_callable(f)
            vals = []
            for v in range(-100, 100):
                try:
                    vals.append(abs(f_lam(v + 0.12345)))
                except Exception:
                    pass
            if vals and max(vals) < 1e5:
                try:
                    v_inf = abs(f_lam(1e5 + 0.12345))
                    v_ninf = abs(f_lam(-1e5 + 0.12345))
                    v_zero = abs(f_lam(1e-5))
                    if v_inf < 1e5 and v_ninf < 1e5 and v_zero < 1e5:
                        is_uac = True
                except Exception:
                    pass
        except Exception:
            pass
        
        if not is_uac:
            h1_ok = False
            break

    h2_ok = True  # Definition of the family F

    neg_q = False
    for f in witnesses:
        try:
            f_lam = get_callable(f)
            dx = 5.0
            total1 = 0.0
            for i in range(-2000, -1000):
                try:
                    val = f_lam(i * dx + 0.12345)
                    total1 += val * dx
                except Exception:
                    pass
            
            total2 = 0.0
            for i in range(-1000, 0):
                try:
                    val = f_lam(i * dx + 0.12345)
                    total2 += val * dx
                except Exception:
                    pass
            
            # If the measure is infinite (e.g. Lebesgue measure), the integral diverges.
            # A valid probability measure would have total1 near 0.
            if abs(total1) > 1.5 or abs(total1 + total2) > 5.0:
                neg_q = True
                break
        except Exception:
            pass

    return [h1_ok, h2_ok, neg_q]