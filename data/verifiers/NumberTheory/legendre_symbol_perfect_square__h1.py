import sympy
from sympy.ntheory import legendre_symbol
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, p) or a dict with keys 'a' and 'p'.
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            p = witness['p']
        else:
            a, p = witness
    except Exception:
        return [False, False, False]

    # H_1: a is an integer (and implicitly p is an integer)
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(p, (int, sympy.Integer))
    except Exception:
        h1 = False

    # H_2: \gcd(a, p) = 1
    try:
        h2 = math.gcd(int(a), int(p)) == 1
    except Exception:
        h2 = False

    # ¬Q: \left(\frac{a^2}{p}\right) \neq 1
    try:
        try:
            # Evaluate the Legendre symbol.
            val = legendre_symbol(int(a)**2, int(p))
            neg_q = (val != 1)
        except ValueError:
            # If p is not a prime, the Legendre symbol is undefined,
            # so the conclusion that it equals 1 is false.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: a is an integer",
    r"H_2: \gcd(a, p) = 1",
    r"¬Q: \left(\frac{a^2}{p}\right) \neq 1"
]

N_HYP = 2
NEG_Q_INDEX = 2