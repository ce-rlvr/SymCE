import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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
    # H_1: G is a finite p-group
    try:
        if not hasattr(witness, 'order'):
            h1 = False
        else:
            o = witness.order
            if callable(o):
                o = o()
            
            if o == 1:
                h1 = True
            else:
                factors = factorint(o)
                h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # ¬Q: The derived series of G does not terminate at the trivial subgroup
    try:
        if hasattr(witness, 'is_solvable'):
            solvable = witness.is_solvable
            if callable(solvable):
                solvable = solvable()
            neg_q = not solvable
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "¬Q: The derived series of G does not terminate at the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1