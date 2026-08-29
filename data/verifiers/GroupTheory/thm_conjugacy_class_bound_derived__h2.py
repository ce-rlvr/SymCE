import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group (and x in G if witness is a tuple)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
            h1_ok = isinstance(G, PermutationGroup) and x in G
        else:
            G = witness
            h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: The size of the conjugacy class of x is strictly greater than the order of the derived subgroup G'
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
            derived_order = G.derived_subgroup().order()
            elements = list(G.generate_dimino())
            conj_class = set()
            for g in elements:
                conj_class.add(g * x * ~g)
            neg_q_ok = len(conj_class) > derived_order
        else:
            G = witness
            derived_order = G.derived_subgroup().order()
            elements = list(G.generate_dimino())
            neg_q_ok = False
            for x in elements:
                conj_class = set()
                for g in elements:
                    conj_class.add(g * x * ~g)
                if len(conj_class) > derived_order:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The size of the conjugacy class of x is strictly greater than the order of the derived subgroup G'"
]

N_HYP = 1
NEG_Q_INDEX = 1