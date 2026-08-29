import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import GF
from sympy.ntheory import isprime

# Top-level setup for standard rings and fields
Z = ZZ
Q = QQ
R = RR
C = CC

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: R is an integral domain
    try:
        if hasattr(witness, 'characteristic'):
            if witness in (ZZ, QQ, RR, CC):
                h1 = True
            elif getattr(witness, 'is_Field', False):
                h1 = True
            elif getattr(witness, 'is_IntegralDomain', False):
                h1 = True
            elif hasattr(witness, 'to_sympy'): # SymPy domains are integral domains
                h1 = True
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The characteristic of R is NOT a prime number
    try:
        char = witness.characteristic
        if callable(char):
            char = char()
        char = int(char)
        neg_q = not isprime(char)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The characteristic of R is not a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1