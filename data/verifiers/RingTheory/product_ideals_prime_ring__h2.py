import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z = sympy.S.Integers
Q = sympy.S.Rationals
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple: (R, I, J)
    where R is a ring, and I, J are ideals (represented by their generators if R is Z or Q).
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I, J = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a prime ring
    try:
        R_str = str(R)
        if R_str in ('Z', 'ZZ', 'Q', 'QQ', 'Integers', 'Rationals', 'M2Z', 'M2Q'):
            h1_ok = True
        elif R in (Z, Q, ZZ, QQ):
            h1_ok = True
        elif hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
            h1_ok = True
        elif hasattr(R, 'is_prime_ring') and R.is_prime_ring:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: J is a non-zero ideal of R
    try:
        if hasattr(J, 'is_zero') and J.is_zero is not None:
            h2_ok = not J.is_zero
        else:
            h2_ok = (J != 0)
    except Exception:
        h2_ok = False

    # ¬Q: The product ideal IJ is the zero ideal
    try:
        prod = I * J
        if hasattr(prod, 'is_zero') and prod.is_zero is not None:
            neg_q_ok = bool(prod.is_zero)
        else:
            neg_q_ok = (prod == 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a prime ring",
    "H_2: J is a non-zero ideal of R",
    "¬Q: The product ideal IJ is the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2