import sympy
from sympy.ntheory import isprime

# Top-level setup
# We represent the ring Z/nZ simply by the integer n.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n > 1:
                # R = Z/nZ is a finite ring, hence it is right Artinian.
                h1 = True
                # Z(R) is the center of R (definitional hypothesis).
                h2 = True
                # Z(R) = Z/nZ is a field if and only if n is prime.
                neg_q = not isprime(n)
        elif witness == sympy.QQ:
            # The field of rational numbers is Artinian.
            h1 = True
            h2 = True
            # Its center is itself, which is a field.
            neg_q = False
        elif witness == sympy.ZZ:
            # The ring of integers is not Artinian.
            h1 = False
            h2 = True
            # Its center is itself, which is not a field.
            neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: Z(R) is the center of R",
    "¬Q: Z(R) is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2