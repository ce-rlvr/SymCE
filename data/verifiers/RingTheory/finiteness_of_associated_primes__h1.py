import sympy

class AbstractIdeal:
    """
    Mock object to represent an ideal in an abstract ring.
    Since SymPy does not natively compute associated primes for arbitrary 
    (especially non-Noetherian) rings, we provide mock objects for the witness.
    """
    def __init__(self, is_proper, finite_assoc_primes):
        self.is_proper = is_proper
        self.finite_assoc_primes = finite_assoc_primes

    @property
    def proper_ideal(self):
        return self.is_proper

    @property
    def has_finite_associated_primes(self):
        return self.finite_assoc_primes

# Top-level setup: named object bindings that the witness expression may reference.
# A standard counterexample to the false conjecture is an ideal in a polynomial ring 
# with infinitely many variables, e.g., R = k[x_1, y_1, x_2, y_2, ...], 
# and I = (x_1^2, x_1 y_1, x_2^2, x_2 y_2, ...). 
# The associated primes are P_n = (x_1, ..., x_{n-1}, y_n, x_{n+1}, ...), 
# of which there are infinitely many.
InfiniteVarsIdeal = AbstractIdeal(is_proper=True, finite_assoc_primes=False)
FiniteVarsIdeal = AbstractIdeal(is_proper=True, finite_assoc_primes=True)
ImproperIdeal = AbstractIdeal(is_proper=False, finite_assoc_primes=True)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: I is a proper ideal of R
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("proper_ideal", False))
        else:
            h1 = bool(getattr(witness, "proper_ideal", False))
    except Exception:
        h1 = False

    # ¬Q: The set of associated prime ideals of I is infinite (i.e. NOT finite)
    try:
        if isinstance(witness, dict):
            finite_assoc = bool(witness.get("has_finite_associated_primes", True))
        else:
            finite_assoc = bool(getattr(witness, "has_finite_associated_primes", True))
        neg_q = not finite_assoc
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: The set of associated prime ideals of I is infinite"
]

N_HYP = 1
NEG_Q_INDEX = 1