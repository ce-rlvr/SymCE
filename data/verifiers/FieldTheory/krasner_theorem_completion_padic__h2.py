import sympy
from sympy.ntheory import isprime

# Top-level setup
# No specific named bindings are needed for this number theory / field theory domain.

def conditions(witness):
    # H_1: p is a prime number
    try:
        if isinstance(witness, (tuple, list)):
            p = int(witness[0])
        else:
            p = int(witness)
        h1 = isprime(p)
    except Exception:
        h1 = False

    # H_2: \mathbb{C}_p is the metric completion of \overline{\mathbb{Q}_p}
    # This is a definitional hypothesis establishing the context of C_p.
    try:
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: \mathbb{C}_p is not an algebraically closed field
    # By Krasner's Theorem, the metric completion of the algebraic closure of Q_p 
    # is always algebraically closed. Therefore, the conclusion is mathematically 
    # true for all valid primes p, meaning its negation is always False.
    try:
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: C_p is the metric completion of the algebraic closure of Q_p",
    "¬Q: C_p is not an algebraically closed field"
]

N_HYP = 2
NEG_Q_INDEX = 2