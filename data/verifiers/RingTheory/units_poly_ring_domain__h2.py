import sympy
from sympy.ntheory import factorint

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        n = None
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
        elif hasattr(witness, 'order') and callable(witness.order):
            n = witness.order()
            
        if n is not None:
            if n == 0:
                h1 = True
                neg_q = False
            elif n == 1:
                h1 = False
                neg_q = False
            else:
                h1 = sympy.isprime(n)
                factors = factorint(n)
                neg_q = any(v > 1 for v in factors.values())
        elif hasattr(witness, 'is_domain'):
            h1 = bool(witness.is_domain)
            neg_q = False
    except Exception:
        pass
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "not Q: The group of units of the polynomial ring is not equal to the group of units of R"
]

N_HYP = 1
NEG_Q_INDEX = 1