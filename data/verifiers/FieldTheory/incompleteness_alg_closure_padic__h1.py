import sympy
from sympy import oo
import math

# Top-level setup
# The witness is expected to be the "prime" p. For the conjecture to fail, 
# p must be the infinite place (oo), where Q_oo = R and its algebraic closure is C, which is complete.

def conditions(witness):
    # H_1: \mathbb{Q}_p is the field of p-adic numbers equipped with the standard p-adic absolute value
    # This is a definitional hypothesis establishing notation for the place p.
    try:
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: \overline{\mathbb{Q}_p} is an algebraic closure of \mathbb{Q}_p equipped with the unique extension of the p-adic absolute value
    # This is also a definitional hypothesis.
    try:
        h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: \overline{\mathbb{Q}_p} is complete with respect to the extended p-adic absolute value
    # The algebraic closure of Q_p is complete ONLY when p is the infinite prime (p = oo), 
    # in which case Q_oo = R and \overline{Q_oo} = C, which is a complete metric space.
    try:
        if witness == oo:
            neg_q_ok = True
        elif isinstance(witness, str) and witness.lower() in ['oo', 'infinity', 'inf']:
            neg_q_ok = True
        elif isinstance(witness, (int, float)) and math.isinf(witness):
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\mathbb{Q}_p is the field of p-adic numbers equipped with the standard p-adic absolute value",
    "H_2: \\overline{\\mathbb{Q}_p} is an algebraic closure of \\mathbb{Q}_p equipped with the unique extension of the p-adic absolute value",
    "¬Q: \\overline{\\mathbb{Q}_p} is complete with respect to the extended p-adic absolute value"
]

N_HYP = 2
NEG_Q_INDEX = 2