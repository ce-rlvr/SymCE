import sympy
from sympy.ntheory import factorint

Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 2:
                h1 = True
                factors = factorint(n)
                is_local = (len(factors) == 1)
                neg_q = not is_local
        elif isinstance(witness, (list, tuple)):
            if len(witness) > 0 and all(isinstance(x, (int, sympy.Integer)) and int(x) >= 2 for x in witness):
                h1 = True
                num_max_ideals = sum(len(factorint(int(x))) for x in witness)
                is_local = (num_max_ideals == 1)
                neg_q = not is_local
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Artinian ring",
    "¬Q: R is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1