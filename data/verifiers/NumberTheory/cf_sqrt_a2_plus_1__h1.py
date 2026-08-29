import sympy
from sympy import sqrt
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    try:
        a = sympy.sympify(witness)
        val = sqrt(a**2 + 1)
        it = continued_fraction_iterator(val)
        
        cf_actual = []
        for _ in range(5):
            try:
                cf_actual.append(next(it))
            except StopIteration:
                break
                
        cf_expected = [a, 2*a, 2*a, 2*a, 2*a]
        
        conclusion_holds = True
        if len(cf_actual) != len(cf_expected):
            conclusion_holds = False
        else:
            for act, exp in zip(cf_actual, cf_expected):
                if act != exp:
                    conclusion_holds = False
                    break
                    
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: The simple continued fraction expansion of sqrt(a^2+1) is not a; 2a, 2a..."]

N_HYP = 0
NEG_Q_INDEX = 0