import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is the torsion subgroup of G",
    "¬Q: T is not a divisible abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, T = witness
        else:
            G = witness
            T = witness
    except Exception:
        return [False, False]

    try:
        # For finite groups, all elements have finite order.
        # Thus, the torsion subgroup is the group itself.
        # We verify that T and G are the same group by checking mutual containment of generators.
        h1 = all(G.contains(g) for g in T.generators) and all(T.contains(g) for g in G.generators)
    except Exception:
        h1 = False

    try:
        # A finitely generated group is divisible if and only if it is the trivial group.
        # Since sympy groups are finitely generated, T is divisible iff T.order() == 1.
        # Therefore, T is a divisible abelian group iff it is abelian and trivial.
        is_div_ab = T.is_abelian and T.order() == 1
        neg_q = not is_div_ab
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]