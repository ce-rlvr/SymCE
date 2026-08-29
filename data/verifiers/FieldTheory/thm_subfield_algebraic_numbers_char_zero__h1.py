import sympy
from sympy import S
from sympy.polys.domains import QQ, RR, CC, ZZ, EX
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: The characteristic of K is zero",
    "¬Q: K does not contain a unique subfield isomorphic to the field of algebraic numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        h1 = False
        if hasattr(witness, 'char'):
            h1 = (witness.char == 0)
        elif hasattr(witness, 'characteristic'):
            h1 = (witness.characteristic == 0)
        elif witness in [S.Rationals, S.Reals, S.Complexes]:
            h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if witness in [S.Rationals, S.Reals]:
            neg_q = True
        elif witness == S.Complexes:
            neg_q = False
        else:
            name = witness.__class__.__name__
            if name in ['RationalField', 'RealField', 'AlgebraicField']:
                neg_q = True
            elif name in ['ComplexField', 'ExpressionDomain']:
                neg_q = False
            elif hasattr(witness, 'domain'):
                domain_name = witness.domain.__class__.__name__
                if domain_name in ['RationalField', 'RealField', 'AlgebraicField']:
                    neg_q = True
                elif domain_name in ['ComplexField', 'ExpressionDomain']:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]