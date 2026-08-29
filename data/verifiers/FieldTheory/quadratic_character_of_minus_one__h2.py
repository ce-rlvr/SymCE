import sympy
import sympy.ntheory

# Top-level setup
# (No specific named bindings required for this field theory conjecture; witnesses are typically integers representing q)

def get_q(witness):
    if hasattr(witness, 'order') and callable(witness.order):
        try:
            return int(witness.order())
        except Exception:
            pass
    if hasattr(witness, 'order'):
        try:
            return int(witness.order)
        except Exception:
            pass
    try:
        return int(witness)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    q = get_q(witness)
    
    # H_1: q is the size of a finite field (prime power)
    try:
        if q is None or q < 2:
            h1 = False
        else:
            factors = sympy.ntheory.factorint(q)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # neg_Q: -1 is a square iff q = 1 mod 4 is FALSE
    try:
        if q is None or q < 2:
            neg_q = False
        else:
            # In a finite field of size q:
            # If q is even (characteristic 2), -1 = 1, which is always a square.
            # If q is odd, -1 is a square iff q = 1 mod 4.
            is_square = (q % 2 == 0) or (q % 4 == 1)
            is_1_mod_4 = (q % 4 == 1)
            neg_q = bool(is_square != is_1_mod_4)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "¬Q: The equivalence (-1 is a square in F_q iff q = 1 mod 4) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1