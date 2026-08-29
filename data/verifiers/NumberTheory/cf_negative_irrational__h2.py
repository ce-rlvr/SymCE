import sympy
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    try:
        h1 = bool(witness.is_irrational)
    except Exception:
        h1 = False

    try:
        it_x = continued_fraction_iterator(witness)
        a = [next(it_x) for _ in range(5)]
        
        it_nx = continued_fraction_iterator(-witness)
        b = [next(it_nx) for _ in range(5)]
            
        expected_b = [-a[0] - 1, 1, a[1] - 1, a[2], a[3]]
        
        neg_q = (b != expected_b)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an irrational number",
    "¬Q: CF of -x is not (-a_0 - 1; 1, a_1 - 1, a_2, a_3, ...)"
]

N_HYP = 1
NEG_Q_INDEX = 1