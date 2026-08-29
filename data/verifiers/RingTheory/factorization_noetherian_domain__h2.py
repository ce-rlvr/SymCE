import sympy
from sympy import Integer, Rational, Poly, Expr
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, (int, Integer)):
            h1 = True
        elif isinstance(witness, Rational):
            h1 = True
        elif isinstance(witness, Poly):
            h1 = witness.domain.is_Field or witness.domain == sympy.ZZ
        elif isinstance(witness, Expr):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, Integer)):
            neg_q = bool(witness == 0 or abs(witness) == 1)
        elif isinstance(witness, Rational) and not witness.is_integer:
            neg_q = True
        elif isinstance(witness, Poly):
            if witness.domain.is_Field:
                neg_q = bool(all(d <= 0 for d in witness.degree_list()))
            else:
                neg_q = bool(witness.is_zero or witness.is_one or witness == -1)
        elif isinstance(witness, Expr):
            simped = sympy.simplify(witness)
            if simped.is_number:
                neg_q = bool(simped == 0 or sympy.Abs(simped) == 1)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian integral domain",
    "¬Q: a cannot be written as a finite product of irreducible elements"
]

N_HYP = 1
NEG_Q_INDEX = 1