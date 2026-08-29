import sympy
from sympy.ntheory import factorint

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        
        if n >= 2:
            h1_ok = True
            h2_ok = True
            factors = factorint(n)
            neg_q_ok = any(exp > 1 for exp in factors.values())
        else:
            h1_ok = False
            h2_ok = False
            neg_q_ok = False
            
    except Exception:
        h1_ok = False
        h2_ok = False
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R satisfies Serre's condition (S1)",
    "¬Q: R is not a reduced ring"
]

N_HYP = 2
NEG_Q_INDEX = 2