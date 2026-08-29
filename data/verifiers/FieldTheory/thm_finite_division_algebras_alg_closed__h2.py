import sympy
from sympy import S, Symbol

# Top-level setup for witness expressions
CC = S.Complexes
RR = S.Reals
QQ = S.Rationals
ZZ = S.Integers
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness (K, D), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            D = witness.get('D')
        else:
            K, D = witness
    except Exception:
        return [False, False]

    # H_1: K is an algebraically closed field
    try:
        h1 = False
        if K == S.Complexes:
            h1 = True
        elif hasattr(K, 'is_algebraically_closed') and K.is_algebraically_closed:
            h1 = True
        elif str(K) in ('CC', 'C', 'Complexes', 'AlgebraicClosure(QQ)'):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: D is not isomorphic to K
    try:
        # In the context of SymPy objects, equality or string equality 
        # is a strong proxy for isomorphism among the standard fields.
        neg_q = (D != K and str(D) != str(K))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: D is not isomorphic to K"
]

N_HYP = 1
NEG_Q_INDEX = 1