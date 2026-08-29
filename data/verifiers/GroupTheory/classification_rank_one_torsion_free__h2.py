import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

F2, x, y = free_group("x y")
F3, a, b, c = free_group("a b c")

def conditions(witness):
    try:
        h1 = None
        if hasattr(witness, 'is_abelian'):
            val = witness.is_abelian
            if val is not None:
                h1 = bool(val)
        
        if h1 is None:
            gens = witness.generators
            h1 = True
            for i in range(len(gens)):
                for j in range(i+1, len(gens)):
                    comm = gens[i]*gens[j]*gens[i]**-1*gens[j]**-1
                    if comm != witness.identity:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        invs = witness.abelian_invariants()
        h2 = (invs.count(0) == 1)
    except Exception:
        h2 = False

    try:
        invs = witness.abelian_invariants()
        has_torsion = any(d > 0 for d in invs)
        rank = invs.count(0)
        is_subgroup_of_Q = (not has_torsion) and (rank <= 1)
        neg_q = not is_subgroup_of_Q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: The rank of G is 1",
    "¬Q: G is not isomorphic to a subgroup of the additive group of rational numbers Q"
]

N_HYP = 2
NEG_Q_INDEX = 2