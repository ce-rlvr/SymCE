import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was likely "x is an element of R".
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'BooleanRing')
            n = witness.get('n')
            x = witness.get('x')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                R, n, x = witness
            elif len(witness) == 2:
                n, x = witness
                R = 'BooleanRing'
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring
    h1_ok = False
    try:
        if isinstance(R, str) and 'boolean' in R.lower():
            h1_ok = True
        elif str(R) in ['GF(2)', 'Z2', 'Z_2', 'F2', 'F_2']:
            h1_ok = True
        elif R == 2:
            h1_ok = True
        elif hasattr(R, 'is_Boolean_ring') and R.is_Boolean_ring:
            h1_ok = True
        elif hasattr(R, '__iter__'):
            count = 0
            all_idempotent = True
            for a in R:
                if a**2 != a:
                    all_idempotent = False
                    break
                count += 1
                if count > 100:  # Prevent infinite loops for infinite domains
                    break
            if all_idempotent and count > 0:
                h1_ok = True
    except Exception:
        pass

    # H_2: n is an integer such that n >= 2
    h2_ok = False
    try:
        if isinstance(n, (int, sympy.Integer)):
            if n >= 2:
                h2_ok = True
        elif isinstance(n, float) and n.is_integer():
            if n >= 2:
                h2_ok = True
    except Exception:
        pass

    # ¬Q: x^n != x
    neg_q_ok = False
    try:
        if bool(x**n != x):
            neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: n is an integer such that n >= 2",
    "¬Q: x^n != x"
]

N_HYP = 2
NEG_Q_INDEX = 2