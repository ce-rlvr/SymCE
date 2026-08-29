import sympy
from sympy import Interval, FiniteSet, Union, Intersection, ProductSet, Reals, Integers, Naturals, oo

# Top-level setup
R = Reals
Z = Integers
N = Naturals

def conditions(witness) -> list[bool]:
    try:
        if witness.is_empty:
            neg_q = True
        else:
            sup = witness.sup
            inf = witness.inf
            if sup == oo or inf == -oo:
                neg_q = True
            else:
                c_sup = witness.contains(sup)
                c_inf = witness.contains(inf)
                if c_sup == True and c_inf == True:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The supremum of the distance between points in K is not attained"
]

N_HYP = 0
NEG_Q_INDEX = 0