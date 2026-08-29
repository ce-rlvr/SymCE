import sympy
from sympy.ntheory import reduced_totient

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        a, n = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: a is an integer
    try:
        h1 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    # H_2: \gcd(a, n) = 1
    try:
        h2 = sympy.gcd(a, n) == 1
    except Exception:
        h2 = False
        
    # H_3: \lambda(n) is the Carmichael function of n
    try:
        lam = reduced_totient(n)
        h3 = True
    except Exception:
        h3 = False
        
    # ¬Q: The modular inverse of a modulo n is not congruent to a^{\lambda(n)-1} \pmod n
    try:
        lam = reduced_totient(n)
        if sympy.gcd(a, n) != 1:
            neg_q = True
        else:
            inv = pow(int(a), -1, int(n))
            val = pow(int(a), int(lam - 1), int(n))
            neg_q = (val - inv) % abs(int(n)) != 0
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: a is an integer",
    r"H_2: \gcd(a, n) = 1",
    r"H_3: \lambda(n) is the Carmichael function of n",
    r"¬Q: The modular inverse of a modulo n is not congruent to a^{\lambda(n)-1} \pmod n"
]

N_HYP = 3
NEG_Q_INDEX = 3