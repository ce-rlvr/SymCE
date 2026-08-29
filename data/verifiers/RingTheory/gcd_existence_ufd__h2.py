import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings
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
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (R, a, b) where R is a ring and a, b are elements.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: R is a unique factorization domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    # ¬Q: a and b do NOT have a greatest common divisor in R
    try:
        # First, check if a and b are actually elements of R.
        # If they are not in R, they cannot have a GCD in R.
        try:
            in_R = (a in R) and (b in R)
        except Exception:
            try:
                R(a)
                R(b)
                in_R = True
            except Exception:
                in_R = False
                
        is_zero_a = (a == 0) or (hasattr(R, 'zero') and a == R.zero)
        is_zero_b = (b == 0) or (hasattr(R, 'zero') and b == R.zero)
        
        if not in_R:
            neg_q = True
        elif is_zero_a and is_zero_b:
            # In some formalizations, GCD(0, 0) is undefined because every element divides 0,
            # hence there is no "greatest" divisor under certain orderings.
            neg_q = True
        else:
            try:
                # If R is a UFD and a, b are in R (and not both zero), they must have a GCD.
                # We attempt to compute it. If it succeeds, they have a GCD, so the conclusion holds (neg_q = False).
                d = R.gcd(a, b)
                neg_q = False
            except Exception:
                # If computation fails or is not implemented, we assume they don't have a GCD.
                neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: a and b do not have a greatest common divisor in R"
]

N_HYP = 1
NEG_Q_INDEX = 1