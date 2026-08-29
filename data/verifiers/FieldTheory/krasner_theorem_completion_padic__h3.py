import sympy

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    
    The witness is expected to be a prime number p.
    """
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(witness))
    except Exception:
        h1 = False

    # H_2: \overline{\mathbb{Q}_p} is the algebraic closure of the p-adic numbers \mathbb{Q}_p 
    # with the extended p-adic absolute value.
    # This is a definitional property that holds for any valid p-adic field setup.
    h2 = True

    # ¬Q: \mathbb{C}_p is not an algebraically closed field
    # By Krasner's Theorem, the completion of the algebraic closure of \mathbb{Q}_p (which is \mathbb{C}_p)
    # is ALWAYS algebraically closed for any prime p.
    # Therefore, the conclusion that \mathbb{C}_p is algebraically closed is always True,
    # meaning its negation is always False.
    neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \\overline{\\mathbb{Q}_p} is the algebraic closure of the p-adic numbers \\mathbb{Q}_p with the extended p-adic absolute value",
    "¬Q: \\mathbb{C}_p is not an algebraically closed field"
]

N_HYP = 2
NEG_Q_INDEX = 2