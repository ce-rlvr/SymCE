import sympy
from sympy import Symbol, Poly

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            a = witness[-1]
        else:
            a = witness
            
        h1 = True
        
        p = Poly(x - a, x)
        if p.is_zero:
            neg_q = True
        elif p.degree() != 1:
            neg_q = True
        else:
            lc = p.LC()
            if abs(lc) != 1:
                neg_q = True
            else:
                neg_q = False
                
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "not Q: quotient ring is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1