import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: Every maximal subgroup of G is a normal subgroup of G
    h1_ok = False
    try:
        if hasattr(witness, 'maximal_subgroups_are_normal'):
            val = witness.maximal_subgroups_are_normal
            h1_ok = bool(val() if callable(val) else val)
        elif hasattr(witness, 'maximal_subgroups'):
            max_subs = witness.maximal_subgroups() if callable(witness.maximal_subgroups) else witness.maximal_subgroups
            all_normal = True
            for H in max_subs:
                if hasattr(witness, 'is_normal'):
                    is_norm = witness.is_normal(H) if callable(witness.is_normal) else witness.is_normal
                    if not is_norm:
                        all_normal = False
                        break
                else:
                    all_normal = False
                    break
            h1_ok = all_normal
        elif hasattr(witness, 'is_nilpotent'):
            # Fallback for finite groups (e.g., SymPy PermutationGroup)
            # By Wielandt's theorem, a finite group has all maximal subgroups normal iff it is nilpotent.
            val = witness.is_nilpotent
            h1_ok = bool(val() if callable(val) else val)
    except Exception:
        h1_ok = False

    # ¬Q: G is not a nilpotent group
    neg_q_ok = False
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            is_nilp = bool(val() if callable(val) else val)
            neg_q_ok = not is_nilp
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Every maximal subgroup of G is a normal subgroup of G",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1