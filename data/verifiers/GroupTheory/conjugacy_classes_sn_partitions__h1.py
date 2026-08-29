import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import npartitions

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks whether the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be interpreted either as the integer `n` or as a permutation group `G` 
    (in case the dropped hypothesis was "G is the symmetric group").
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True
            n = int(witness)
            try:
                grp = SymmetricGroup(n)
                num_classes = len(grp.conjugacy_classes())
                p_n = npartitions(n)
                neg_q = bool(num_classes != p_n)
            except Exception:
                # If SymmetricGroup(n) is undefined (e.g., n <= 0), the conclusion fails to hold.
                neg_q = True
                
        elif isinstance(witness, PermutationGroup):
            h1 = True
            n = witness.degree
            try:
                num_classes = len(witness.conjugacy_classes())
                p_n = npartitions(n)
                neg_q = bool(num_classes != p_n)
            except Exception:
                neg_q = True
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let S_n be the symmetric group on n letters",
    "¬Q: The number of conjugacy classes of S_n is not equal to p(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1