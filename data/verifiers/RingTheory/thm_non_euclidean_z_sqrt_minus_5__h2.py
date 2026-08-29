import sympy
from sympy import ZZ, QQ
from sympy.abc import x
from sympy.polys.domains.domain import Domain

# Top-level setup: named object bindings that the witness expression may reference.
Z_ring = ZZ
Q_field = QQ

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is an integral domain, then R is not a Euclidean domain."
    """
    # H_1: R is an integral domain
    try:
        h1 = False
        if isinstance(witness, Domain):
            h1 = True
        elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: R is a Euclidean domain (negation of "R is not a Euclidean domain")
    try:
        neg_q = False
        if witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            neg_q = True
        elif isinstance(witness, Domain):
            if witness.is_Field:
                neg_q = True
            elif witness == sympy.ZZ:
                neg_q = True
            elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
                # A univariate polynomial ring over a field is a Euclidean domain
                if witness.domain.is_Field and len(witness.symbols) == 1:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1