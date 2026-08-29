import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, list):
            witness = PermutationGroup(witness)
    except Exception:
        pass

    # H_1: G is an abelian group
    try:
        prop = getattr(witness, 'is_abelian')
        h1 = bool(prop() if callable(prop) else prop)
    except Exception:
        h1 = False

    # H_2: X is a non-empty set
    try:
        h2 = bool(int(witness.degree) > 0)
    except Exception:
        h2 = False

    # H_3: The action of G on X is faithful
    try:
        # A PermutationGroup's natural action on its domain is faithful by definition.
        if isinstance(witness, PermutationGroup):
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: The action of G on X is transitive
    try:
        prop = getattr(witness, 'is_transitive')
        h4 = bool(prop() if callable(prop) else prop)
    except Exception:
        h4 = False

    # ¬Q: The action of G on X is not regular
    try:
        all_trivial = True
        for i in range(int(witness.degree)):
            stab = witness.stabilizer(i)
            stab_order = stab.order() if callable(stab.order) else stab.order
            if int(stab_order) > 1:
                all_trivial = False
                break
        
        # The conclusion states the action is regular (stabilizer of every point is trivial).
        # The negated conclusion means at least one stabilizer is non-trivial.
        neg_q = not all_trivial
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: X is a non-empty set",
    "H_3: The action of G on X is faithful",
    "H_4: The action of G on X is transitive",
    "¬Q: The action of G on X is not regular"
]

N_HYP = 4
NEG_Q_INDEX = 4