import sympy
from sympy import oo

# Top-level setup
# (No specific named objects needed for this number theory / field theory domain)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a prime number p (or a dictionary/tuple containing p).
    """
    # Extract p from the witness if it's wrapped in a dict or tuple
    if isinstance(witness, dict):
        p = witness.get('p', witness)
    elif isinstance(witness, (list, tuple)) and len(witness) > 0:
        p = witness[0]
    else:
        p = witness

    # H_1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    # H_2: \overline{\mathbb{Q}_p} is an algebraic closure of \mathbb{Q}_p equipped 
    # with the unique extension of the p-adic absolute value.
    # This is a definitional mathematical statement that is inherently true.
    h2_ok = True

    # ¬Q: \overline{\mathbb{Q}_p} is complete with respect to the extended p-adic absolute value.
    # Mathematically, for any finite prime p, the algebraic closure of Q_p is of infinite degree
    # and is never complete (its completion is C_p, which is strictly larger).
    # Thus, the conclusion "is not complete" is always TRUE for any prime p, making its negation FALSE.
    # (If p were somehow the infinite prime oo, Q_oo is R, its algebraic closure is C, which IS complete).
    try:
        if p == oo:
            neg_Q_ok = True
        else:
            neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [h1_ok, h2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \overline{\mathbb{Q}_p} is an algebraic closure of \mathbb{Q}_p equipped with the unique extension of the p-adic absolute value",
    "¬Q: \overline{\mathbb{Q}_p} is complete with respect to the extended p-adic absolute value"
]

N_HYP = 2
NEG_Q_INDEX = 2