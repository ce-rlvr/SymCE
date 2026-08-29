import sympy
from sympy import Symbol
from sympy.polys.domains import RR, CC, QQ, ZZ
from sympy.polys.domains.field import Field

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # H_1: R is the field of real numbers (implicitly, the witness E is a field)
        h1 = isinstance(witness, Field) or getattr(witness, 'is_Field', False) or witness in (sympy.S.Reals, sympy.S.Complexes)
    except Exception:
        h1 = False

    try:
        # ¬Q: E is NOT isomorphic to either R or C
        # In the context of SymPy domains, we check if the witness is exactly the R or C domain.
        is_R_or_C = witness in (RR, CC, sympy.S.Reals, sympy.S.Complexes) or str(witness) in ('RR', 'CC', 'R', 'C', 'Reals', 'Complexes')
        neg_q = not is_R_or_C
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is the field of real numbers",
    "¬Q: E is not isomorphic to either R or C"
]

N_HYP = 1
NEG_Q_INDEX = 1