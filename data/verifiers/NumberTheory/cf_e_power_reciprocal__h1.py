import sympy
from sympy import exp, Rational
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    try:
        k = Rational(witness)
        
        form_cf = [1]
        n = 0
        while len(form_cf) < 15:
            form_cf.append((2*n + 1)*k - 1)
            form_cf.append(1)
            form_cf.append(1)
            n += 1
        form_cf = form_cf[:15]
        
        if k == 0:
            neg_q = True
        else:
            val = exp(1/k).evalf(400)
            it = continued_fraction_iterator(val)
            actual_cf = []
            try:
                for _ in range(15):
                    actual_cf.append(next(it))
            except StopIteration:
                pass
            
            neg_q = (actual_cf != form_cf)
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: The simple continued fraction expansion of e^(1/k) does not match the formula"]
N_HYP = 0
NEG_Q_INDEX = 0