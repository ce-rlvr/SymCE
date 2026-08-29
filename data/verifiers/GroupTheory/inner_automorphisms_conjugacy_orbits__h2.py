import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: The orbits of the action of Inn(G) on G are NOT exactly the conjugacy classes of G
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.generate())
            
            # Compute the conjugacy classes of G
            conjugacy_classes = set()
            for x in elements:
                cclass = frozenset(g * x * ~g for g in elements)
                conjugacy_classes.add(cclass)
                    
            # Compute the orbits of the action of Inn(G) on G
            # Inn(G) consists of inner automorphisms phi_g(x) = g * x * g^-1
            orbits = set()
            for x in elements:
                orbit = frozenset(g * x * ~g for g in elements)
                orbits.add(orbit)
                    
            q = (conjugacy_classes == orbits)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The orbits of the action of Inn(G) on G are not exactly the conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1