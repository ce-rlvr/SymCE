import sympy
from sympy import S

# Top-level setup
# No specific named objects are required for this conjecture beyond SymPy's built-in S.Complexes.

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # H_1: Let C be the field of complex numbers.
        # We check if the witness represents the complex numbers.
        h1_ok = (witness == S.Complexes or str(witness) in ['C', 'CC', 'Complexes', 'S.Complexes'])
    except Exception:
        h1_ok = False

    try:
        # Conclusion: C is the algebraic closure of R.
        # The algebraic closure of the real numbers is exactly the field of complex numbers.
        # The conclusion holds if the witness is the complex numbers.
        q_ok = (witness == S.Complexes or str(witness) in ['C', 'CC', 'Complexes', 'S.Complexes'])
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: C is the field of complex numbers",
    "¬Q: C is not the algebraic closure of R"
]

N_HYP = 1
NEG_Q_INDEX = 1