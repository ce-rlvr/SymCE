import sympy
from sympy import Rational

CONDITION_LABELS = [
    "H_1: x is a rational number",
    "H_2: a is a finite simple continued fraction expansion of x",
    "not Q: x does not have exactly one other finite simple continued fraction expansion given by a_0, a_1, ..., a_n - 1, 1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        x, a = witness
    except Exception:
        return [False, False, False]
        
    x_val = None
    
    # H1: x is a rational number
    try:
        if isinstance(x, float):
            x_val = sympy.Rational(x)
            h1 = True
        elif isinstance(x, (int, sympy.Integer, sympy.Rational)):
            x_val = sympy.Rational(x)
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: a is a finite simple continued fraction expansion of x
    try:
        if not isinstance(a, (list, tuple)):
            h2 = False
        elif len(a) < 1:
            h2 = False
        elif not all(isinstance(c, (int, sympy.Integer)) for c in a):
            h2 = False
        elif not all(c >= 1 for c in a[1:]):
            h2 = False
        else:
            val = sympy.Rational(a[-1], 1)
            for c in reversed(a[:-1]):
                val = c + 1 / val
            h2 = (val == x_val)
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        if x_val is None:
            neg_q = False
        else:
            num, den = x_val.p, x_val.q
            cf1 = []
            while den != 0:
                q = num // den
                cf1.append(q)
                num, den = den, num - q * den
            
            if len(cf1) == 1:
                cf2 = [cf1[0] - 1, 1]
            else:
                cf2 = cf1[:-1] + [cf1[-1] - 1, 1]
                    
            valid_scfs = {tuple(cf1), tuple(cf2)}
            
            other_proposed = tuple(list(a[:-1]) + [a[-1] - 1, 1])
            
            is_simple = True
            if len(other_proposed) > 1:
                if not all(c >= 1 for c in other_proposed[1:]):
                    is_simple = False
                    
            if not is_simple:
                conclusion_holds = False
            else:
                conclusion_holds = (valid_scfs == {tuple(a), other_proposed}) and (other_proposed != tuple(a))
                
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]