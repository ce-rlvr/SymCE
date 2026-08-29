import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: I is equal to its own radical in R",
    "¬Q: The extended ideal is not equal to its own radical in the polynomial ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        h1_ok = bool(witness.is_ideal())
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(witness.is_radical())
    except Exception:
        h2_ok = False

    try:
        if hasattr(witness, "extended_ideal"):
            q_ok = bool(witness.extended_ideal().is_radical())
        elif hasattr(witness, "is_extended_radical"):
            q_ok = bool(witness.is_extended_radical())
        elif hasattr(witness, "extended_ideal_is_radical"):
            q_ok = bool(witness.extended_ideal_is_radical())
        else:
            q_ok = True
    except Exception:
        q_ok = True

    neg_q_ok = not q_ok

    return [h1_ok, h2_ok, neg_q_ok]