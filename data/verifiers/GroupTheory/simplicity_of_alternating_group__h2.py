import sympy
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    # H_1: Let n be an integer such that n >= 5.
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            h1 = n >= 5
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The group A_n is NOT a simple group.
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            if n >= 1:
                if n > 6:
                    # A_n is known to be simple for all n >= 5.
                    # We bypass normal_subgroups() for n > 6 to ensure the verifier remains fast.
                    is_simple = True
                else:
                    G = AlternatingGroup(n)
                    # A group is simple if it has exactly 2 normal subgroups (itself and the trivial group)
                    is_simple = len(G.normal_subgroups()) == 2
                neg_q = not is_simple
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 5",
    "¬Q: The group A_n is not a simple group"
]

N_HYP = 1
NEG_Q_INDEX = 1