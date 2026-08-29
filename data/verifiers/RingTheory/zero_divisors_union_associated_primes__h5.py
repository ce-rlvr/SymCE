import sympy
from sympy import symbols

# Top-level setup
# We don't need specific named groups or matrices for this ring theory conjecture.
# The witness will be a dictionary containing the ring, ideal, primary decomposition, etc.
# We will evaluate the properties based on the provided witness.

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    "Zero Divisors as Union of Associated Primes"
    
    Hypotheses:
      - R is a commutative ring with identity
      - R is a Noetherian ring
      - I is a proper ideal of R
      - I = q_1 \cap ... \cap q_n is an irredundant primary decomposition of I
      
    Conclusion:
      An element x in R is a zero divisor on R/I if and only if x belongs to the union of the associated primes P_1 \cup ... \cup P_n
    """
    
    # H1: R is a commutative ring with identity
    try:
        h1 = bool(witness.get("is_commutative_ring_with_identity", False))
    except Exception:
        h1 = False

    # H2: R is a Noetherian ring
    try:
        h2 = bool(witness.get("is_noetherian", False))
    except Exception:
        h2 = False

    # H3: I is a proper ideal of R
    try:
        h3 = bool(witness.get("is_proper_ideal", False))
    except Exception:
        h3 = False

    # H4: I = q_1 \cap ... \cap q_n is an irredundant primary decomposition of I
    try:
        h4 = bool(witness.get("is_irredundant_primary_decomposition", False))
    except Exception:
        h4 = False

    # ¬Q: The conclusion FAILS at the witness.
    # The conclusion states: x is a zero divisor on R/I iff x is in the union of associated primes.
    # The negation is: there exists an x such that (x is a zero divisor on R/I and x is NOT in the union of associated primes)
    # OR (x is NOT a zero divisor on R/I and x IS in the union of associated primes).
    try:
        # The witness should provide a boolean indicating if the conclusion holds.
        # We want the negation of the conclusion.
        conclusion_holds = bool(witness.get("conclusion_holds", True))
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: I is a proper ideal of R",
    "H_4: I = q_1 \\cap ... \\cap q_n is an irredundant primary decomposition of I",
    "¬Q: The set of zero divisors on R/I is NOT exactly the union of the associated primes"
]

N_HYP = 4
NEG_Q_INDEX = 4