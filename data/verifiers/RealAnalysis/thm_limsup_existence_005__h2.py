import sympy
from sympy import Symbol, oo

# Top-level setup
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    # H1: (a_n) is a sequence of real numbers
    h1_ok = False
    try:
        if hasattr(witness, 'subs'):
            h1_ok = True
            for i in range(1, 21):
                val = witness.subs(n, i).evalf()
                if not val.is_real or not val.is_finite:
                    h1_ok = False
                    break
        elif isinstance(witness, (int, float)):
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The limit superior of (a_n) is NOT a finite real number
    neg_q_ok = False
    try:
        L = sympy.limit(witness, n, oo)
        if type(L).__name__ == 'AccumBounds':
            limsup = L.max
            if limsup == oo or limsup == -oo:
                neg_q_ok = True
            elif getattr(limsup, 'is_finite', None) is False:
                neg_q_ok = True
            elif getattr(limsup, 'is_finite', None) is True:
                neg_q_ok = False
            else:
                raise ValueError("Cannot determine finiteness of AccumBounds max")
        elif type(L).__name__ == 'Limit':
            raise ValueError("Unevaluated limit")
        else:
            if L == oo or L == -oo:
                neg_q_ok = True
            elif getattr(L, 'is_finite', None) is False:
                neg_q_ok = True
            elif getattr(L, 'is_finite', None) is True:
                neg_q_ok = False
            else:
                raise ValueError("Cannot determine finiteness")
    except Exception:
        # Fallback for unevaluated or indeterminate limits
        try:
            vals = []
            for i in range(1000, 1100):
                v = witness.subs(n, i).evalf()
                if v.is_real:
                    vals.append(float(v))
            
            if vals:
                if max(vals) > 500 or min(vals) < -500:
                    vals2 = []
                    for i in range(10000, 10100):
                        v2 = witness.subs(n, i).evalf()
                        if v2.is_real:
                            vals2.append(float(v2))
                    if vals2 and (max(vals2) > 5000 or min(vals2) < -5000):
                        neg_q_ok = True
        except Exception:
            pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "¬Q: The limit superior of (a_n) is not a finite real number"
]

N_HYP = 1
NEG_Q_INDEX = 1