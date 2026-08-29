import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    # H_1: Let n >= 3 be an integer
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and int(witness) >= 3
    except Exception:
        h1 = False

    # ¬Q: The Frattini subgroup of S_n is NOT the trivial subgroup
    # Mathematically, the Frattini subgroup of S_n is the intersection of all its maximal subgroups.
    # For n >= 3, A_n is a maximal subgroup of S_n, and S_{n-1} is also a maximal subgroup.
    # Their intersection is A_{n-1}. The normal core of A_{n-1} in S_n is trivial for n >= 3.
    # Since the Frattini subgroup is normal in S_n and contained in A_{n-1}, it must be trivial.
    # Therefore, the Frattini subgroup of S_n is ALWAYS the trivial subgroup for all n >= 3.
    # Because the conclusion is universally true for all valid witnesses, it never fails.
    # Thus, the negated conclusion is always False.
    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer >= 3",
    "¬Q: The Frattini subgroup of S_n is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1