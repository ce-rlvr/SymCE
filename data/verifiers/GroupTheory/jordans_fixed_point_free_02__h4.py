import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # We interpret the witness as a SymPy PermutationGroup.
    # A PermutationGroup G naturally acts on the finite set X = {0, 1, ..., G.degree - 1}.
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a finite set
    try:
        # The domain of a PermutationGroup is always finite.
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: |X| >= 2
    try:
        h3 = isinstance(witness, PermutationGroup) and witness.degree >= 2
    except Exception:
        h3 = False

    # ¬Q: Every element in G has at least one fixed point in X
    # (Negation of: There exists at least one element g in G such that g.x != x for all x in X)
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            neg_q = True
            for g in witness.generate():
                # g.support() returns the list of points moved by g.
                # If len(g.support()) == witness.degree, g moves all points (i.e., has no fixed points).
                if len(g.support()) == witness.degree:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "H_3: |X| >= 2",
    "¬Q: Every element in G has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3