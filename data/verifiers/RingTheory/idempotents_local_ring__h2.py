import sympy
from sympy import ZZ, QQ
import itertools

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = n >= 2
            for x in range(2, n):
                if (x * x) % n == x:
                    neg_q = True
                    break
                    
        elif isinstance(witness, (tuple, list)) and all(isinstance(x, (int, sympy.Integer)) for x in witness):
            h1 = all(int(x) >= 2 for x in witness)
            ranges = [list(range(int(n))) for n in witness]
            for elem in itertools.product(*ranges):
                is_idemp = all((e * e) % int(n) == e for e, n in zip(elem, witness))
                is_zero = all(e == 0 for e in elem)
                is_one = all(e == 1 for e in elem)
                if is_idemp and not is_zero and not is_one:
                    neg_q = True
                    break
                    
        elif witness in (ZZ, QQ):
            h1 = True
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: There exists an idempotent element in R other than 0 and 1"
]

N_HYP = 1
NEG_Q_INDEX = 1