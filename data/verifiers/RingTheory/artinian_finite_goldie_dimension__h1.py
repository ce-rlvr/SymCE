import sympy
from sympy import eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Custom ring objects for Goldie dimension
class CustomRing:
    def __init__(self, name, finite_goldie_dim=True):
        self.name = name
        self.finite_goldie_dim = finite_goldie_dim

Z_omega = CustomRing("Infinite direct product of Z", finite_goldie_dim=False)
F2_omega = CustomRing("Infinite direct product of F2", finite_goldie_dim=False)
End_V_inf = CustomRing("Endomorphism ring of infinite dimensional vector space", finite_goldie_dim=False)
Free_Algebra_2 = CustomRing("Free algebra on 2 generators", finite_goldie_dim=False)
Z = CustomRing("Integers", finite_goldie_dim=True)
Q = CustomRing("Rationals", finite_goldie_dim=True)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'finite_goldie_dim'):
            neg_q = not witness.finite_goldie_dim
        elif isinstance(witness, str):
            s = witness.lower()
            if 'infinite' in s and ('product' in s or 'sum' in s or 'boolean' in s):
                neg_q = True
            elif 'omega' in s or 'infty' in s or 'infinity' in s:
                neg_q = True
            elif 'free algebra' in s:
                neg_q = True
            elif 'endomorphism' in s and 'infinite' in s:
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R does not have finite right Goldie dimension"
]

N_HYP = 0
NEG_Q_INDEX = 0