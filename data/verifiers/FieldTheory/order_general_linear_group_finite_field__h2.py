import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def conditions(witness) -> list[bool]:
    """
    Given a witness (n, q), checks if it satisfies the remaining hypotheses
    and fails the conclusion.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
        elif hasattr(witness, 'n') and hasattr(witness, 'q'):
            n = witness.n
            q = witness.q
        else:
            n, q = witness
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field with q elements
    try:
        q_val = int(q)
        if q_val >= 2 and q_val == q:
            factors = sympy.ntheory.factorint(q_val)
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: GL_n(F_q) is the group of n x n invertible matrices
    try:
        n_val = int(n)
        h2 = (n_val == n and n_val >= 0)
    except Exception:
        h2 = False

    # neg_Q: The order of GL_n(F_q) is not q^{n(n-1)/2} \prod_{i=1}^n (q^i - 1)
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            n_val = int(n)
            q_val = int(q)
            
            # Calculate the true order of GL_n(F_q)
            true_order = 1
            for i in range(n_val):
                true_order *= (q_val**n_val - q_val**i)
            
            # Calculate the formula given in the conclusion
            formula = q_val**(n_val * (n_val - 1) // 2)
            for i in range(1, n_val + 1):
                formula *= (q_val**i - 1)
            
            neg_q = (true_order != formula)
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: GL_n(F_q) is the group of n x n invertible matrices",
    "¬Q: The order of GL_n(F_q) is not q^{n(n-1)/2} \\prod_{i=1}^n (q^i - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2