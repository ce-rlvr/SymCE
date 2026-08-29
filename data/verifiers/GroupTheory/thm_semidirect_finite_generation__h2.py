import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# --- Top-level setup ---

def _is_fg(grp):
    """Helper to determine if a group is finitely generated."""
    if hasattr(grp, "is_finitely_generated"):
        return grp.is_finitely_generated
    # SymPy PermutationGroups and FpGroups are finitely generated
    if hasattr(grp, "generators"):
        return True
    return False

class AbstractGroup:
    """A mock group class to represent infinite groups with known properties."""
    def __init__(self, name, is_finitely_generated):
        self.name = name
        self.is_finitely_generated = is_finitely_generated

    def __str__(self):
        return self.name

class SemidirectProductGroup(AbstractGroup):
    """Represents the internal semidirect product of N and H."""
    def __init__(self, N, H):
        name_N = getattr(N, "name", str(N))
        name_H = getattr(H, "name", str(H))
        super().__init__(
            name=f"{name_N} ⋊ {name_H}",
            is_finitely_generated=(_is_fg(N) and _is_fg(H))
        )
        self.normal_subgroup = N
        self.complement_subgroup = H

    def is_internal_semidirect_product_of(self, N, H):
        return self.normal_subgroup is N and self.complement_subgroup is H

# Standard finite algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Custom objects for infinite groups (since SymPy only supports finite/finitely-presented groups)
Z_inf = AbstractGroup("Z", is_finitely_generated=True)
Q_inf = AbstractGroup("Q", is_finitely_generated=False)
R_inf = AbstractGroup("R", is_finitely_generated=False)
Z2_inf = AbstractGroup("Z2", is_finitely_generated=True)

# A valid counterexample: Q ⋊ Z2
Q_rtimes_Z2 = SemidirectProductGroup(Q_inf, Z2_inf)
R_rtimes_Z2 = SemidirectProductGroup(R_inf, Z2_inf)


# --- Verifier ---

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: H is finitely generated",
    "¬Q: G is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        if hasattr(G, "is_internal_semidirect_product_of"):
            h1 = bool(G.is_internal_semidirect_product_of(N, H))
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: H is finitely generated
    try:
        h2 = bool(_is_fg(H))
    except Exception:
        h2 = False

    # ¬Q: G is not finitely generated (Conclusion fails)
    try:
        neg_q = not bool(_is_fg(G))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]