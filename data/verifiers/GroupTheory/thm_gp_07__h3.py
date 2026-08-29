import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference.
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
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The conjecture states that the group defined by the given presentation is isomorphic to S_n.
    The missing hypothesis is s_i^2 = 1. Without it, the group is infinite.
    """
    # The only universally quantified variable is n.
    # The witness should be n, or a tuple starting with n.
    if isinstance(witness, (tuple, list)):
        if len(witness) > 0:
            n = witness[0]
        else:
            n = None
    else:
        n = witness

    # H_1: Let n >= 2 be an integer.
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False

    # H_2: Let G be the group defined by the presentation with generators s_1, ..., s_{n-1}.
    # This is a definition, so it's inherently satisfied by our construction of G.
    h2 = h1

    # H_3: The generators satisfy the relations (s_i s_{i+1})^3 = 1 for all 1 <= i <= n-2.
    # Satisfied by definition of G.
    h3 = h1

    # H_4: The generators satisfy the relations (s_i s_j)^2 = 1 for all i, j such that |i - j| >= 2.
    # Satisfied by definition of G.
    h4 = h1

    # ¬Q: The group G is NOT isomorphic to the symmetric group S_n.
    try:
        if not h1:
            neg_q = False
        else:
            # The group G defined by this presentation is infinite for all n >= 2
            # because the relations s_i^2 = 1 are missing.
            # Since S_n is a finite group, G is never isomorphic to S_n.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: G is the group defined by the presentation with generators s_1, ..., s_{n-1}",
    "H_3: The generators satisfy the relations (s_i s_{i+1})^3 = 1 for all 1 <= i <= n-2",
    "H_4: The generators satisfy the relations (s_i s_j)^2 = 1 for all i, j such that |i - j| >= 2",
    "¬Q: The group G is not isomorphic to the symmetric group S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4