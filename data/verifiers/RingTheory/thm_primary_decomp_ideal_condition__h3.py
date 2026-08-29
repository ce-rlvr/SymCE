import sympy
from sympy.ntheory import factorint
import math

Z = sympy.S.Integers

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        n = None
        if isinstance(witness, (tuple, list, set)):
            ints = []
            for item in witness:
                try:
                    ints.append(int(item))
                except Exception:
                    pass
            if ints:
                n = ints[0]
                for i in ints[1:]:
                    n = math.gcd(n, i)
        else:
            n = int(witness)
            
        if n is not None:
            h1 = True
            h2 = abs(n) != 1
            
            if n == 0:
                neg_q = False
            else:
                factors = factorint(abs(n))
                neg_q = len(factors) > 1
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q is a proper ideal of R",
    "¬Q: Q is not a primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2