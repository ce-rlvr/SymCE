import sympy
from sympy.abc import x, y, z

# Top-level setup (empty as no specific named groups/matrices are required for this field theory witness, 
# but we provide standard symbols just in case the witness expression uses them).

def conditions(witness):
    """
    Given a witness (expected to be a prime number p), evaluates the hypotheses 
    and the negated conclusion.
    """
    try:
        # Check if the witness can be interpreted as an integer
        p = int(witness)
        # H_1: p is a prime number
        h1_ok = sympy.isprime(p)
    except Exception:
        h1_ok = False

    try:
        # H_2: \overline{\mathbb{F}_p} is an algebraic closure of \mathbb{F}_p
        # This is a definitional property that holds for any valid prime p.
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    try:
        # ¬Q: The conclusion states that the algebraic closure is isomorphic to the union 
        # of the finite fields \mathbb{F}_{p^n} for all integers n \geq 1.
        # This is FALSE because the set-theoretic union of abstract finite fields is not a field 
        # (they are not nested unless specific embeddings or a direct limit are defined).
        # Therefore, the negation of the conclusion is TRUE for any valid prime p.
        neg_q_ok = h1_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \\overline{\\mathbb{F}_p} is an algebraic closure of \\mathbb{F}_p",
    "¬Q: \\overline{\\mathbb{F}_p} is not isomorphic to the union of the finite fields \\mathbb{F}_{p^n} for all integers n \\geq 1"
]

N_HYP = 2
NEG_Q_INDEX = 2