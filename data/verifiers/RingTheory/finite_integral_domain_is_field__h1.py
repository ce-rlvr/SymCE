import sympy
from sympy import isprime, Integer

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard finite rings Z/nZ represented as integers.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R has finitely many elements, then R is a field."
    
    We interpret an integer n >= 1 as the finite ring Z/nZ.
    """
    h1_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, bool):
            pass
        elif isinstance(witness, (int, Integer)):
            n = int(witness)
            if n >= 1:
                h1_ok = True
                # Z/nZ is a field iff n is prime.
                neg_q_ok = not isprime(n)
        elif isinstance(witness, str):
            w_upper = witness.upper()
            if w_upper.startswith("Z") and w_upper[1:].isdigit():
                n = int(w_upper[1:])
                if n >= 1:
                    h1_ok = True
                    neg_q_ok = not isprime(n)
        elif witness in [ZZ, QQ, RR, CC]:
            h1_ok = False
            neg_q_ok = not witness.is_Field
        elif hasattr(witness, 'is_finite') and hasattr(witness, 'is_Field'):
            h1_ok = bool(witness.is_finite)
            neg_q_ok = not bool(witness.is_Field)
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has finitely many elements",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1