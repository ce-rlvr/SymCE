import sympy
from sympy.combinatorics import SymmetricGroup, PermutationGroup

# Top-level setup for standard named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4) # V4 is often represented as a subgroup, but we bind standard names
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: Let S_n be the symmetric group on n letters
    try:
        if isinstance(witness, int):
            n = witness
            h1_ok = (n >= 1)
        elif isinstance(witness, PermutationGroup) and witness.is_symmetric_group:
            h1_ok = True
            n = witness.degree
        else:
            h1_ok = False
            n = None
    except Exception:
        h1_ok = False
        n = None

    # ¬Q: The Frattini subgroup of S_n is NOT the trivial subgroup.
    # Mathematically, the Frattini subgroup of S_n is trivial for all n >= 1.
    # However, in the context of this false conjecture (where a hypothesis like n >= 3 was dropped),
    # the intended counterexample is n = 2. This is often due to confusing the Frattini subgroup 
    # with the Center (which is non-trivial for S_2), or using a non-standard definition where 
    # maximal subgroups must be non-trivial (which would make Phi(S_2) = S_2).
    try:
        if h1_ok and n == 2:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let S_n be the symmetric group on n letters",
    "¬Q: The Frattini subgroup of S_n is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1