import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Inn(G) is a cyclic group
    # Inn(G) is isomorphic to G/Z(G). We check if G/Z(G) is cyclic.
    try:
        if not h1:
            h2 = False
        else:
            Z = witness.center()
            n = witness.order() // Z.order()
            if n == 1:
                h2 = True
            else:
                prime_factors = list(factorint(n).keys())
                h2 = False
                # Check if there is an element g in G such that g Z(G) generates G/Z(G)
                for g in witness.elements:
                    is_gen = True
                    for p in prime_factors:
                        if (g**(n // p)) in Z:
                            is_gen = False
                            break
                    if is_gen:
                        h2 = True
                        break
    except Exception:
        h2 = False

    # neg_Q: G is not an abelian group, or Inn(G) is not the trivial group
    try:
        if not h1:
            neg_q = False
        else:
            is_abelian = witness.is_abelian
            inn_is_trivial = (witness.order() == witness.center().order())
            q = is_abelian and inn_is_trivial
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Inn(G) is a cyclic group",
    "¬Q: G is not an abelian group, or Inn(G) is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2