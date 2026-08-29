import sympy
from sympy import symbols
from sympy.abc import x, y, z

def check_attr(obj, attrs, default):
    if isinstance(obj, tuple) and len(obj) == 2:
        if isinstance(obj[1], dict) or hasattr(obj[1], attrs[0]):
            obj = obj[1]
        elif isinstance(obj[0], dict) or hasattr(obj[0], attrs[0]):
            obj = obj[0]
            
    if isinstance(obj, dict):
        for attr in attrs:
            if attr in obj:
                return bool(obj[attr])
    else:
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    return bool(val())
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    
    Remaining hypotheses:
      - P is a prime ideal of R
    Conclusion:
      - P_x is a prime ideal of R_x
    """
    h1_ok = False
    try:
        h1_ok = check_attr(witness, ["P_is_prime", "is_P_prime", "is_prime_ideal", "P_prime", "is_prime"], False)
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        q_ok = check_attr(witness, ["Px_is_prime", "is_Px_prime", "is_poly_prime_ideal", "Px_prime", "is_poly_prime"], True)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: P is a prime ideal of R", "not Q: P_x is not a prime ideal of R_x"]
N_HYP = 1
NEG_Q_INDEX = 1