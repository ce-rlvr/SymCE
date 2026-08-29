import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    # H_1: F is finitely generated
    try:
        # In SymPy, any PermutationGroup is finite, hence finitely generated.
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: F does NOT admit an injective group homomorphism into SL(2, R)
    try:
        if isinstance(witness, PermutationGroup):
            # A finite group embeds in SL(2, R) if and only if it is cyclic.
            # (Any finite subgroup of SL(2, R) is conjugate to a subgroup of SO(2), which is abelian and its finite subgroups are cyclic).
            # Thus, it does NOT embed if and only if it is NOT cyclic.
            is_abelian = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
            if not is_abelian:
                is_cyclic = False
            else:
                if hasattr(witness, 'is_cyclic'):
                    is_cyclic = witness.is_cyclic() if callable(witness.is_cyclic) else witness.is_cyclic
                else:
                    order = witness.order() if callable(witness.order) else witness.order
                    if order > 2000:
                        is_cyclic = False
                    else:
                        is_cyclic = any((g.order() if callable(g.order) else g.order) == order for g in witness.generate())
            neg_q_ok = not is_cyclic
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is finitely generated",
    "¬Q: F does not admit an injective group homomorphism into SL(2, R)"
]

N_HYP = 1
NEG_Q_INDEX = 1