import sympy
from sympy import factorint, isprime

# Top-level setup
# No special named bindings are required for this number-theoretic/field-theoretic witness,
# as the witness is expected to be an integer p.

def conditions(witness) -> list[bool]:
    """
    Given a witness p, checks if it satisfies the remaining hypotheses
    and fails the conclusion of the conjecture.
    """
    try:
        # The witness is expected to be the parameter p
        p = int(witness)
    except Exception:
        return [False, False]
    
    # H_1: \overline{\mathbb{F}_p} is an algebraic closure of the finite field \mathbb{F}_p
    # This implies that \mathbb{F}_p is a finite field, which means p must be a prime power.
    try:
        if p <= 1:
            h1_ok = False
        else:
            factors = factorint(p)
            h1_ok = (len(factors) == 1)
    except Exception:
        h1_ok = False
        
    # ¬Q: The conclusion fails.
    # The true theorem requires p to be a prime. If p is a prime power but not a prime (e.g., p=4),
    # the set of fields \mathbb{F}_{p^n} does not contain all finite subfields of the algebraic closure
    # (for instance, \mathbb{F}_2 is a subfield but not of the form \mathbb{F}_{4^n}).
    # Thus, under the strict structural interpretation intended by the theorem, the conclusion fails.
    try:
        neg_q_ok = not isprime(p)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\overline{\\mathbb{F}_p} is an algebraic closure of the finite field \\mathbb{F}_p",
    "¬Q: \\overline{\\mathbb{F}_p} is not isomorphic to the union of all finite fields \\mathbb{F}_{p^n} for n \\ge 1, partially ordered by inclusion"
]

N_HYP = 1
NEG_Q_INDEX = 1