import sympy
import sympy.abc
import sympy.polys

# Top-level setup
class Ring:
    """Mock class for a mathematical ring."""
    def __init__(self, name="R"):
        self.name = name

class Ideal:
    """Mock class for an ideal in a ring."""
    def __init__(self, ring, is_proper, associated_primes):
        self.ring = ring
        self.is_proper = is_proper
        self.associated_primes = associated_primes

# A known counterexample to the conjecture:
# R = k[x_1, x_2, ...] / (x_1^2, x_2^2, ...)
# I = (0)
# The ring R is non-Noetherian, and the proper ideal I has no associated primes.
R_counterexample = Ring("k[x_1, x_2, ...] / (x_1^2, x_2^2, ...)")
I_counterexample = Ideal(R_counterexample, is_proper=True, associated_primes=[])

def conditions(witness) -> list[bool]:
    # H_1: I is a proper ideal in R
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_proper', False))
        elif isinstance(witness, tuple) and len(witness) == 2:
            h1 = bool(witness[1].is_proper)
        else:
            h1 = bool(witness.is_proper)
    except Exception:
        h1 = False

    # ¬Q: The set of associated primes Ass(R/I) is empty
    try:
        if isinstance(witness, dict):
            neg_q = len(witness.get('associated_primes', [None])) == 0
        elif isinstance(witness, tuple) and len(witness) == 2:
            neg_q = len(witness[1].associated_primes) == 0
        else:
            neg_q = len(witness.associated_primes) == 0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal in R",
    "¬Q: The set of associated primes Ass(R/I) is empty"
]

N_HYP = 1
NEG_Q_INDEX = 1