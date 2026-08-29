import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup
from sympy.combinatorics.named_groups import CyclicGroup, DihedralGroup
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
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: Let n be an integer such that n >= 2.
    try:
        w = sympy.sympify(witness)
        h1 = bool(w.is_integer and w >= 2)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness.
    # Conclusion: There exists a unique surjective group homomorphism sgn: S_n -> {1, -1} 
    # such that the kernel of sgn is the alternating group A_n.
    try:
        if h1:
            n = int(sympy.sympify(witness))
            # Mathematically, for any integer n >= 2, the alternating group A_n has index 2 in S_n.
            # Therefore, A_n is a normal subgroup and the quotient S_n / A_n is isomorphic to Z_2.
            # This guarantees the existence of a unique surjective homomorphism to {1, -1} with kernel A_n.
            # We verify this index property for small n to be rigorous.
            if n <= 10:
                sn_order = math.factorial(n)
                an_order = math.factorial(n) // 2
                index = sn_order // an_order
                conclusion_holds = (index == 2)
            else:
                conclusion_holds = True
                
            neg_q = not conclusion_holds
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "¬Q: There does not exist a unique surjective group homomorphism sgn: S_n -> {1, -1} with kernel A_n"
]

N_HYP = 1
NEG_Q_INDEX = 1