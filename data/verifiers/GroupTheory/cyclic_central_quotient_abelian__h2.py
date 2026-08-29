import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/Z(G) is a cyclic group",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The quotient group G/Z(G) is a cyclic group
    h2 = False
    try:
        if h1:
            Z = witness.center()
            if Z.order() == witness.order():
                # If Z(G) = G, then G/Z(G) is the trivial group, which is cyclic.
                h2 = True
            else:
                # G/Z(G) is cyclic iff there exists g in G such that <Z(G), g> = G
                Z_gens = list(Z.generators)
                target_order = witness.order()
                count = 0
                for g in witness.elements:
                    count += 1
                    if count > 2000:  # Safety limit for performance
                        break
                    if PermutationGroup(Z_gens + [g]).order() == target_order:
                        h2 = True
                        break
    except Exception:
        h2 = False

    # ¬Q: G is not an abelian group
    neg_q = False
    try:
        if h1:
            neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]