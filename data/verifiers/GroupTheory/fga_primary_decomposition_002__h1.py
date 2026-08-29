import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        # The conclusion states G is isomorphic to a direct product of cyclic groups 
        # of prime power order. Since a direct product of cyclic groups is abelian,
        # any non-abelian group cannot satisfy this.
        # For finite groups (which sympy PermutationGroup represents), 
        # the Fundamental Theorem of Finite Abelian Groups guarantees that 
        # ALL finite abelian groups satisfy the conclusion.
        # Thus, the conclusion fails if and only if G is not abelian.
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is not isomorphic to a direct product of cyclic groups whose orders are prime powers (e.g., G is non-abelian)"
]

N_HYP = 0
NEG_Q_INDEX = 0