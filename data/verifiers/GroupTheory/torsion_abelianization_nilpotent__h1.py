import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, free_group, FpGroup, PermutationGroup

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

class InfiniteDihedralGroup:
    def abelian_invariants(self):
        return [2, 2]
    
    def is_torsion_group(self):
        return False

D_inf_custom = InfiniteDihedralGroup()

def is_abelianization_torsion(G):
    if hasattr(G, 'abelian_invariants'):
        invs = G.abelian_invariants()
        return (0 not in invs)
    if type(G).__name__ == 'PermutationGroup':
        return True
    if hasattr(G, 'is_abelianization_torsion'):
        val = G.is_abelianization_torsion
        return val() if callable(val) else val
    return False

def is_torsion_group(G):
    if hasattr(G, 'is_torsion_group'):
        val = G.is_torsion_group
        return val() if callable(val) else val
    if type(G).__name__ == 'PermutationGroup':
        return True
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_abelianization_torsion(witness))
    except Exception:
        h1 = False

    try:
        neg_q = not bool(is_torsion_group(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: G/G' is a torsion group", "¬Q: G is not a torsion group"]
N_HYP = 1
NEG_Q_INDEX = 1