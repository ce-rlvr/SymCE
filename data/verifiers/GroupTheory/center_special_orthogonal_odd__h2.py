import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any odd integer n >= 3, the center of SO(n, R) is trivial.
    This is true if R is a field or an integral domain (like the Reals), but false for 
    general commutative rings (e.g., R = Z/4Z, where the center is non-trivial).
    """
    
    # H_1: Let n be an odd integer such that n >= 3
    try:
        if isinstance(witness, tuple):
            n = int(witness[0])
        elif hasattr(witness, 'shape'):
            n = witness.shape[0]
        else:
            n = int(witness)
        h1 = (n % 2 == 1) and (n >= 3)
    except Exception:
        h1 = False

    # ¬Q: The center of SO(n, R) is NOT the trivial group containing only the identity matrix
    try:
        if isinstance(witness, tuple):
            n = int(witness[0])
            R = witness[1] if len(witness) > 1 else None
        elif hasattr(witness, 'shape'):
            n = witness.shape[0]
            R = None
        else:
            n = int(witness)
            R = None
            
        if n == 1:
            # SO(1, R) is always trivial, so its center is trivial.
            neg_q = False
        else:
            if R is not None:
                R_str = str(R).lower()
                # If R is explicitly a standard domain/field, the center IS trivial,
                # so the conclusion holds (neg_Q is False).
                trivial_domains = ['real', 'rr', 'ℝ', 'int', 'zz', 'qq', 'complex', 'cc', 'field', 'rational']
                if any(x in R_str for x in trivial_domains):
                    neg_q = False
                else:
                    # For rings with zero divisors (like Z/4Z), the center is non-trivial.
                    neg_q = True
            elif hasattr(witness, 'shape'):
                # If the witness is a specific matrix counterexample, it must not be the identity.
                if bool(witness != eye(n)):
                    neg_q = True
                else:
                    neg_q = False
            else:
                # If only n is provided, the conclusion fails because there exists a ring R 
                # (e.g., Z/4Z) where the center of SO(n, R) is non-trivial for any odd n >= 3.
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd integer such that n >= 3",
    "¬Q: The center of SO(n, R) is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1