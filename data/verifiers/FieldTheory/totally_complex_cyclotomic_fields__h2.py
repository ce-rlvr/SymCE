import sympy

# Top-level setup
# No specific named objects are required for this number theory/field theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    Hypothesis:
      H_1: n is an integer strictly greater than 2
      
    Conclusion:
      Q: Q(zeta_n) has no real embeddings, making it a totally complex number field.
      neg_Q: Q(zeta_n) has at least one real embedding.
      
    Mathematically, the n-th cyclotomic field Q(zeta_n) has a real embedding 
    if and only if n = 1 or n = 2.
    """
    # Evaluate H_1: n is an integer strictly greater than 2
    try:
        if isinstance(witness, bool) or not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = n > 2
    except Exception:
        h1 = False

    # Evaluate neg_Q: Q(zeta_n) has at least one real embedding
    try:
        if isinstance(witness, bool) or not isinstance(witness, (int, sympy.Integer)):
            neg_q = False
        else:
            n = int(witness)
            if n < 1:
                # Cyclotomic fields are typically defined for n >= 1
                neg_q = False
            else:
                # Q(zeta_n) has a real embedding iff n = 1 or n = 2
                neg_q = (n <= 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "¬Q: Q(zeta_n) has at least one real embedding (is not totally complex)"
]

N_HYP = 1
NEG_Q_INDEX = 1