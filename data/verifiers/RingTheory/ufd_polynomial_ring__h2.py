import sympy
import sympy.ntheory

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, int) and not isinstance(witness, bool):
            if witness > 1:
                h1 = True
                # Z_n[x] is a UFD iff n is prime (since Z_n must be a field/domain)
                neg_q = not sympy.ntheory.isprime(witness)
        elif hasattr(witness, 'is_UFD'):
            h1 = True
            neg_q = not witness.is_UFD
    except Exception:
        pass
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = ["H_1: R is a commutative ring", "¬Q: R poly ring is not a UFD"]

N_HYP = 1
NEG_Q_INDEX = 1