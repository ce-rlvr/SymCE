import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.polys.domains import ZZ, QQ

class AlgebraicRing:
    def __init__(self, name, is_integrally_closed):
        self.name = name
        self.is_integrally_closed = is_integrally_closed
        self.frac_field = None

    def __repr__(self):
        return self.name

# Fields
Q = AlgebraicRing("Q", True)
Q.frac_field = Q

Q_sqrt_5 = AlgebraicRing("Q(sqrt(5))", True)
Q_sqrt_5.frac_field = Q_sqrt_5

Q_sqrt_m3 = AlgebraicRing("Q(sqrt(-3))", True)
Q_sqrt_m3.frac_field = Q_sqrt_m3

Q_i = AlgebraicRing("Q(i)", True)
Q_i.frac_field = Q_i

k_t = AlgebraicRing("k(t)", True)
k_t.frac_field = k_t

# Integrally closed domains
Z = AlgebraicRing("Z", True)
Z.frac_field = Q

Z_i = AlgebraicRing("Z[i]", True)
Z_i.frac_field = Q_i

# Non-integrally closed domains
Z_sqrt_5 = AlgebraicRing("Z[sqrt(5)]", False)
Z_sqrt_5.frac_field = Q_sqrt_5

Z_sqrt_m3 = AlgebraicRing("Z[sqrt(-3)]", False)
Z_sqrt_m3.frac_field = Q_sqrt_m3

k_t2_t3 = AlgebraicRing("k[t^2, t^3]", False)
k_t2_t3.frac_field = k_t


def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, K = witness
        else:
            R = witness
            if hasattr(R, 'frac_field'):
                K = R.frac_field
            elif hasattr(R, 'get_field'):
                K = R.get_field()
            else:
                K = None

        # H1: K is the field of fractions of R
        if hasattr(R, 'frac_field'):
            h1 = (K is not None) and (K == R.frac_field)
        elif hasattr(R, 'get_field'):
            h1 = (K is not None) and (K == R.get_field())
        else:
            h1 = False

        # neg_Q: R is NOT integrally closed in K
        if hasattr(R, 'is_integrally_closed'):
            neg_q = not R.is_integrally_closed
        else:
            # Standard SymPy domains like ZZ, QQ are integrally closed
            neg_q = False

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]


CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "¬Q: R is not integrally closed in K"
]

N_HYP = 1
NEG_Q_INDEX = 1