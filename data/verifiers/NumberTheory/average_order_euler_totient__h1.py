import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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
    Checks if the witness is a counterexample to the false conjecture.
    The dropped hypothesis from the true theorem is x >= 2 (or x > 1).
    Without it, the asymptotic formula fails at x = 1 because the error term 
    O(x log x) evaluates to 0, forcing an exact equality which is false.
    """
    # Extract x and phi from the witness
    if isinstance(witness, tuple) and len(witness) == 2:
        x, phi = witness
    else:
        x = witness
        phi = sympy.totient

    # H_1: \phi(n) denotes Euler's totient function
    try:
        if phi == sympy.totient:
            h1_ok = True
        else:
            h1_ok = all(phi(n) == sympy.totient(n) for n in range(1, 10))
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails at the witness
    try:
        # Evaluate the error bound x * log(x)
        try:
            err = float(x * sympy.log(x))
        except Exception:
            err = 1.0  # Fallback for invalid/complex values
            
        # If x * log(x) == 0 (which happens at x = 1), the error term must be exactly 0.
        # We can definitively check if the conclusion fails by checking exact equality.
        if err == 0.0:
            if x < 1:
                lhs = 0
            else:
                lhs = sum(phi(n) for n in range(1, int(math.floor(x)) + 1))
            
            rhs_sym = 3 / sympy.pi**2 * (x**2)
            
            # The conclusion fails if LHS != RHS
            neg_q_ok = bool(sympy.sympify(lhs) != rhs_sym)
        else:
            # For x > 1, the error bound is > 0, so the Big-O term can absorb the difference.
            # We cannot easily falsify the asymptotic statement for a single point.
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\phi(n) denotes Euler's totient function",
    "¬Q: The asymptotic formula \\sum_{n \\le x} \\phi(n) = \\frac{3}{\\pi^2} x^2 + O(x \\log x) fails at x"
]

N_HYP = 1
NEG_Q_INDEX = 1