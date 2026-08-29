import sympy
from sympy.combinatorics import PermutationGroup, free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Free groups (F2 is the standard counterexample for this conjecture)
F2_tuple = free_group("x, y")
F2 = F2_tuple[0]
x, y = F2_tuple[1:]

F3_tuple = free_group("a, b, c")
F3 = F3_tuple[0]
a, b, c = F3_tuple[1:]

def conditions(witness):
    # H_1: G is a finitely generated group
    try:
        if hasattr(witness, 'generators'):
            h1 = len(witness.generators) >= 0
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G is torsion-free
    try:
        if type(witness).__name__ == 'FreeGroup':
            h2 = True
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            h2 = True
        elif hasattr(witness, 'abelian_invariants'):
            is_ab = witness.is_abelian
            if callable(is_ab):
                is_ab = is_ab()
            if is_ab:
                invs = witness.abelian_invariants()
                h2 = all(i == 0 for i in invs)
            else:
                h2 = False
        elif isinstance(witness, PermutationGroup):
            h2 = (witness.order() == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G is not a free abelian group
    try:
        if hasattr(witness, 'is_abelian'):
            is_ab = witness.is_abelian
            if callable(is_ab):
                is_ab = is_ab()
        else:
            gens = witness.generators
            is_ab = all(g * h == h * g for g in gens for h in gens)
        
        if not is_ab:
            # If it is not abelian, it cannot be a free abelian group
            neg_q = True
        else:
            # If it is abelian, it is free abelian iff it is torsion-free
            if hasattr(witness, 'abelian_invariants'):
                invs = witness.abelian_invariants()
                has_torsion = any(i != 0 for i in invs)
                neg_q = has_torsion
            elif type(witness).__name__ == 'FreeGroup':
                # A FreeGroup is abelian iff its rank is <= 1, in which case it is free abelian
                neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G is torsion-free",
    "¬Q: G is not a free abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2