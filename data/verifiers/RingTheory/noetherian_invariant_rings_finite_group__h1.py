import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    def get_prop(prop, default=False):
        if isinstance(witness, dict):
            return witness.get(prop, default)
        return getattr(witness, prop, default)

    try:
        h1 = bool(get_prop('R_is_finitely_generated_commutative_A_algebra'))
    except Exception:
        h1 = False

    try:
        h2 = bool(get_prop('G_is_finite_group') and get_prop('G_acts_on_R_by_A_algebra_automorphisms'))
    except Exception:
        h2 = False

    try:
        q = bool(get_prop('R_G_is_finitely_generated_A_algebra') and get_prop('R_G_is_Noetherian_ring'))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a finitely generated commutative A-algebra",
    "H_2: G is a finite group acting on R by A-algebra automorphisms",
    "¬Q: R^G is not a finitely generated A-algebra or R^G is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2