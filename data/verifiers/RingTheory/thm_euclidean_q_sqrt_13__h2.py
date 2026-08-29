import sympy

CONDITION_LABELS = [
    "H_1: K = Q(sqrt(13)) is a real quadratic field",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, int):
            d = witness
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            d = int(witness)
        else:
            d = 13
            
        h1 = (d == 13)
        
        euclidean_ds = {2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 73}
        
        neg_q = d not in euclidean_ds
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]