import sympy
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A3 = AlternatingGroup(3)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = int(witness) >= 1
        elif isinstance(witness, PermutationGroup):
            n = witness.degree
            if n >= 1:
                h1 = bool(witness == AlternatingGroup(n))
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)):
            G = AlternatingGroup(int(witness))
        elif isinstance(witness, PermutationGroup):
            G = witness
        else:
            G = None
        
        if G is not None:
            neg_q = bool(G.is_solvable)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is an alternating group A_n (or an integer n >= 1)",
    "¬Q: A_n is solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1
