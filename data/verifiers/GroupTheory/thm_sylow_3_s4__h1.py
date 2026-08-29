import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if not hasattr(witness, 'sylow_subgroup'):
            return [False]
        if not hasattr(witness, 'generate'):
            return [False]
        if hasattr(witness, 'order') and witness.order() > 5000:
            return [False]
            
        P = witness.sylow_subgroup(3)
        P_elements = list(P.generate())
        conjugates = set()
        
        for g in witness.generate():
            conj = frozenset([g * x * ~g for x in P_elements])
            conjugates.add(conj)
            
        n_3 = len(conjugates)
        neg_q = bool(n_3 != 4)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The number of Sylow 3-subgroups of G is not exactly 4"
]

N_HYP = 0
NEG_Q_INDEX = 0
