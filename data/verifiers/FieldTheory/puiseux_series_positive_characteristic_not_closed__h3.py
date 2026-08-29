import sympy
import sympy.ntheory
from sympy import CC

# Top-level setup
# No specific named objects are strictly required for this field theory conjecture,
# but we provide CC (Complex Field) as a standard algebraically closed field.

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: The characteristic of K is a prime p > 0",
    "¬Q: The field L is algebraically closed"
]

def conditions(witness):
    """
    Given a witness object, checks if it satisfies the hypotheses and falsifies the conclusion.
    Since SymPy cannot natively represent algebraically closed fields of positive characteristic,
    the witness can be a dictionary or object specifying the properties, or a tuple (p, L).
    """
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if isinstance(witness, dict):
            H1 = bool(witness.get("K_is_algebraically_closed", False))
            p = int(witness.get("K_char", 0))
            H2 = sympy.ntheory.isprime(p) and p > 0
            neg_Q = bool(witness.get("L_is_algebraically_closed", False))
            if not neg_Q and witness.get("L") == CC:
                neg_Q = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            p, L = witness
            H1 = True  # Implicitly K is the algebraic closure of F_p
            H2 = sympy.ntheory.isprime(int(p)) and int(p) > 0
            neg_Q = (L == CC or L is True or getattr(L, "is_algebraically_closed", False) or str(L).lower() in ["algebraically closed", "true"])
        else:
            H1 = bool(getattr(witness, "K_is_algebraically_closed", False))
            p = int(getattr(witness, "K_char", 0))
            H2 = sympy.ntheory.isprime(p) and p > 0
            neg_Q = bool(getattr(witness, "L_is_algebraically_closed", False))
            if not neg_Q and getattr(witness, "L", None) == CC:
                neg_Q = True
    except Exception:
        pass

    return [H1, H2, neg_Q]