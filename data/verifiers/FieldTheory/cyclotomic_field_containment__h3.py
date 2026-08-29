import sympy
from sympy import lcm
from sympy.ntheory import totient

# No specific named bindings are required for this number theory / field theory conjecture.
# Witnesses are expected to be tuples or dicts containing the integers m and n.

def get_mn(witness):
    """Helper to extract m and n from various witness formats."""
    if hasattr(witness, 'm') and hasattr(witness, 'n'):
        return witness.m, witness.n
    elif isinstance(witness, dict):
        return witness['m'], witness['n']
    else:
        return witness[0], witness[1]

def conditions(witness) -> list[bool]:
    # H_1: m and n are positive integers
    try:
        m, n = get_mn(witness)
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h1 = False

    # H_2: m divides n
    try:
        m, n = get_mn(witness)
        h2 = isinstance(m, int) and isinstance(n, int) and m != 0 and (n % m == 0)
    except Exception:
        h2 = False

    # ¬Q: The cyclotomic field Q(zeta_m) is NOT a subfield of Q(zeta_n)
    # Q(zeta_m) is a subfield of Q(zeta_n) iff Q(zeta_m)Q(zeta_n) = Q(zeta_n)
    # The compositum is Q(zeta_{lcm(m,n)}). Thus, it is a subfield iff 
    # the degree phi(lcm(m, n)) equals the degree phi(n).
    try:
        m, n = get_mn(witness)
        if not (isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0):
            neg_q = False
        else:
            neg_q = bool(totient(lcm(m, n)) != totient(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: m divides n",
    "¬Q: Q(zeta_m) is not a subfield of Q(zeta_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2