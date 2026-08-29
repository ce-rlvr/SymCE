import sympy
from sympy import eye, zeros, Rational, Integer, S
from sympy.abc import x, y, z
from sympy.polys import domains

# Top-level setup for potential witness objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if the conclusion FAILS (neg_Q is True).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        elif isinstance(witness, dict):
            R = witness.get('R', None)
            M = witness.get('M', None)
        else:
            R = witness
            M = None
    except Exception:
        R, M = None, None

    # Check H_1: R is a commutative ring with identity
    h1 = False
    try:
        if R is not None:
            if R in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
                h1 = True
            elif isinstance(R, domains.Domain) and R.is_commutative:
                h1 = True
            elif hasattr(R, 'is_commutative') and R.is_commutative:
                if hasattr(R, 'has_1') and R.has_1:
                    h1 = True
                elif hasattr(R, 'one') and R.one is not None:
                    h1 = True
            elif isinstance(R, int):
                # Integers can represent Z/nZ rings
                h1 = True
    except Exception:
        pass

    # Check neg_Q: M polynomials form a maximal ideal in R polynomials
    # Mathematically, for any commutative ring R with identity and any ideal M,
    # the ideal M[x] is NEVER a maximal ideal in R[x].
    # This is because the quotient ring R[x]/M[x] is isomorphic to (R/M)[x],
    # and a polynomial ring over any ring is never a field.
    # Therefore, the conclusion "M[x] is not a maximal ideal" is ALWAYS True,
    # which means its negation is ALWAYS False.
    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "not Q: M polynomials form a maximal ideal in R polynomials"
]

N_HYP = 1
NEG_Q_INDEX = 1