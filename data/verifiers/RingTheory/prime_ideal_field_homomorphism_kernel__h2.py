import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    The witness is expected to represent a ring R and an ideal P.
    Common representations:
      - An integer n: represents R = Z and P = nZ.
      - A tuple (m, n): represents R = mZ and P = nZ.
      - A tuple (R, P) of objects where R has an 'is_commutative' attribute.
    """
    try:
        # Parse the witness into ring R and ideal P representations
        if isinstance(witness, int):
            m, n = 1, witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                m, n = witness[0], witness[1]
            else:
                # Fallback for object-based witnesses (e.g., sympy rings/ideals)
                R_obj, P_obj = witness
                h1 = getattr(R_obj, 'is_commutative', True)
                # The conjecture fails exactly when P = R (the zero ring R/R embeds in a field 
                # via the zero homomorphism, but R is not a proper/prime ideal of itself).
                neg_q = (P_obj == R_obj)
                return [bool(h1), bool(neg_q)]
        else:
            return [False, False]
            
        # H1: R is a commutative ring
        # mZ is always a commutative ring.
        h1 = True
        
        # Check if P = nZ is actually an ideal of R = mZ
        if m == 0:
            is_ideal = (n == 0)
        else:
            is_ideal = (n % m == 0)
            
        if not is_ideal:
            # If P is not an ideal, it cannot be a prime ideal, and ker(phi) = P is impossible.
            # Thus LHS = False and RHS = False, meaning the biconditional holds (neg_Q is False).
            return [h1, False]
            
        # The conclusion states: P is a prime ideal iff R/P embeds in a field.
        # LHS: P is a prime ideal. This is true iff P is proper and R/P is an integral domain.
        # RHS: R/P embeds in a field. This is true iff R/P has no zero divisors.
        # Since any commutative ring without zero divisors embeds in its field of fractions,
        # RHS is true iff P is a prime ideal OR P = R (where R/P = {0} embeds via the zero map).
        # Therefore, the biconditional fails (neg_Q is True) exactly when P = R.
        neg_q = (abs(n) == abs(m))
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: It is not true that P is a prime ideal if and only if there exists a field F and a ring homomorphism phi: R -> F such that ker(phi) = P"
]

N_HYP = 1
NEG_Q_INDEX = 1