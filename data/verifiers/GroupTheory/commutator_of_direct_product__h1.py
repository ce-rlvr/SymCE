import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a group
    try:
        h_is_group = isinstance(H, PermutationGroup)
    except Exception:
        h_is_group = False

    # Conclusion: The commutator subgroup (G × H)' is equal to G' × H'
    try:
        # In SymPy, G * H for PermutationGroups computes the direct product.
        # .derived_subgroup() computes the commutator subgroup.
        lhs = (G * H).derived_subgroup()
        rhs = G.derived_subgroup() * H.derived_subgroup()
        q = (lhs == rhs)
    except Exception:
        # If G is not a group, the operations will raise an exception,
        # meaning the conclusion is ill-defined (and thus fails).
        q = False

    neg_q = not q

    return [h_is_group, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "¬Q: The commutator subgroup (G × H)' is not equal to G' × H' (or is ill-defined)"
]

N_HYP = 1
NEG_Q_INDEX = 1