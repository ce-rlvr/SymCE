import sympy
from sympy import S

Q = S.Rationals
Z = S.Integers

def conditions(witness):
    h1 = False
    try:
        if witness == S.Rationals:
            h1 = True
        elif witness == S.Integers:
            h1 = True
        elif isinstance(witness, (list, set, tuple)):
            if all(isinstance(x, (int, sympy.Rational)) or (hasattr(x, 'is_Rational') and x.is_Rational) for x in witness):
                h1 = True
        elif hasattr(witness, 'is_subset'):
            subset_check = witness.is_subset(S.Rationals)
            if subset_check == True:
                if witness in (S.Naturals, S.Naturals0, S.EmptySet):
                    h1 = False
                else:
                    h1 = True
        elif isinstance(witness, str) and witness.lower() in ['q', 'rationals', 's.rationals', 'sympy.s.rationals']:
            h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if witness == S.Rationals:
            neg_q = True
        elif witness == S.Integers:
            neg_q = False
        elif isinstance(witness, (list, set, tuple)):
            neg_q = False
        elif isinstance(witness, str) and witness.lower() in ['q', 'rationals', 's.rationals', 'sympy.s.rationals']:
            neg_q = True
        elif hasattr(witness, 'is_subset'):
            subset_check = witness.is_subset(S.Rationals)
            if subset_check == True:
                if getattr(witness, 'is_FiniteSet', False) or getattr(witness, 'is_finite', False):
                    neg_q = False
                elif witness not in (S.Integers, S.Naturals, S.Naturals0, S.EmptySet):
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the additive group of rational numbers Q",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1