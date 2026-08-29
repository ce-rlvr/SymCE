import sympy
from sympy import S, Complement, ProductSet, Interval, Union, Intersection

# Top-level setup
# No special algebraic objects needed for Real Analysis sets.

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        def is_uncountable(A):
            if A == S.Reals:
                return True
            if isinstance(A, Interval):
                return A.start != A.end
            if isinstance(A, Union):
                return any(is_uncountable(arg) for arg in A.args)
            return False

        def check_not_sigma_compact(U):
            if isinstance(U, Complement):
                A, B = U.args
                if B in (S.Rationals, getattr(S, 'Algebraics', None)):
                    if is_uncountable(A):
                        return True
            if isinstance(U, ProductSet):
                return any(check_not_sigma_compact(arg) for arg in U.args)
            return False

        neg_q = bool(check_not_sigma_compact(witness))
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: U is not sigma-compact"
]

N_HYP = 0
NEG_Q_INDEX = 0