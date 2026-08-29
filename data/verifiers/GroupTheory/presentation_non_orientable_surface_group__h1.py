import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    # Extract G if witness is a tuple
    G = witness
    if isinstance(witness, tuple):
        for item in witness:
            if hasattr(item, 'abelian_invariants'):
                G = item
                break

    # H_1: G is the fundamental group \pi_1(N_k)
    h1_ok = False
    try:
        if hasattr(G, 'abelian_invariants'):
            invs = G.abelian_invariants()
            # Accept groups with abelianizations matching surface groups or free groups
            if all(x == 0 for x in invs):
                h1_ok = True
            elif invs.count(2) == 1 and invs.count(0) == len(invs) - 1:
                h1_ok = True
    except Exception:
        pass

    # ¬Q: G does NOT admit the presentation \langle a_1, \dots, a_k \mid a_1^2 \dots a_k^2 = 1 \rangle
    neg_q = False
    try:
        if hasattr(G, 'abelian_invariants'):
            invs = G.abelian_invariants()
            # The presentation in the conclusion has abelianization Z^{k-1} x Z_2.
            # If G's abelianization is different, it cannot admit this presentation.
            if len(invs) == 0:
                neg_q = False
            elif invs.count(2) == 1 and invs.count(0) == len(invs) - 1:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        pass

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is the fundamental group \\pi_1(N_k)",
    "¬Q: G does not admit the presentation \\langle a_1, a_2, \\dots, a_k \\mid a_1^2 a_2^2 \\dots a_k^2 = 1 \\rangle"
]

N_HYP = 1
NEG_Q_INDEX = 1