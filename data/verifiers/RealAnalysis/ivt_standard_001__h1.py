import sympy
from sympy import Symbol, solveset, S, Interval

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    # H_1: k is a real number strictly between f(a) and f(b)
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            k = witness['k']
        else:
            f, a, b, k = witness
            
        if isinstance(f, str):
            f = sympy.sympify(f, locals={'x': x})
            
        if callable(f):
            fa = float(f(a))
            fb = float(f(b))
        else:
            fa = float(f.subs(x, a))
            fb = float(f.subs(x, b))
            
        kf = float(k)
        
        h1_ok = (fa < kf < fb) or (fb < kf < fa)
    except Exception:
        h1_ok = False

    # ¬Q: There does not exist a point c in the open interval (a, b) such that f(c) = k
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            k = witness['k']
        else:
            f, a, b, k = witness
            
        if isinstance(f, str):
            f = sympy.sympify(f, locals={'x': x})
            
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
            
        af = float(a)
        bf = float(b)
        k_sym = sympy.sympify(k)
        
        lower = min(af, bf)
        upper = max(af, bf)
        
        if af >= bf:
            # The open interval (a, b) is empty if a >= b.
            # Thus, there trivially does not exist c in (a, b) such that f(c) = k.
            neg_q_ok = True
        else:
            sol = solveset(f_expr - k_sym, x, domain=Interval.open(lower, upper))
            if sol == S.EmptySet:
                neg_q_ok = True
            elif isinstance(sol, sympy.ConditionSet):
                # If sympy cannot solve it, we conservatively return False to avoid false positives.
                neg_q_ok = False
            else:
                # Non-empty FiniteSet, Interval, Union, etc. implies solutions exist.
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: k is a real number strictly between f(a) and f(b)",
    "¬Q: There does not exist a point c in the open interval (a, b) such that f(c) = k"
]

N_HYP = 1
NEG_Q_INDEX = 1