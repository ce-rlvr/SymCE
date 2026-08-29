import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.homomorphisms import GroupHomomorphism
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
    # Extract G, H, f
    try:
        if isinstance(witness, GroupHomomorphism):
            f = witness
            G = f.domain
            H = f.codomain
        elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'f'):
            G = witness.G
            H = witness.H
            f = witness.f
        elif isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
        else:
            G, H, f = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        def check_group(grp):
            if hasattr(grp, 'is_group') and grp.is_group:
                return True
            if isinstance(grp, (PermutationGroup, FreeGroup, FpGroup)):
                return True
            return False
        
        h1 = check_group(G) and check_group(H)
    except Exception:
        h1 = False

    # H_2: f: G -> H is a surjective group homomorphism
    try:
        if isinstance(f, GroupHomomorphism):
            h2 = (f.domain == G) and (f.codomain == H) and f.is_surjective()
        else:
            is_hom = False
            is_surj = False
            if hasattr(f, 'is_homomorphism'):
                is_hom = f.is_homomorphism() if callable(f.is_homomorphism) else f.is_homomorphism
            elif hasattr(f, 'is_group_homomorphism'):
                is_hom = f.is_group_homomorphism() if callable(f.is_group_homomorphism) else f.is_group_homomorphism
            
            if hasattr(f, 'is_surjective'):
                is_surj = f.is_surjective() if callable(f.is_surjective) else f.is_surjective
                
            h2 = bool(is_hom and is_surj)
    except Exception:
        h2 = False

    # neg_Q: H does NOT satisfy the ascending chain condition on normal subgroups
    try:
        def check_acc(grp):
            if hasattr(grp, 'satisfies_acc_normal'):
                val = grp.satisfies_acc_normal() if callable(grp.satisfies_acc_normal) else grp.satisfies_acc_normal
                return bool(val)
            if hasattr(grp, 'is_Noetherian'):
                val = grp.is_Noetherian() if callable(grp.is_Noetherian) else grp.is_Noetherian
                return bool(val)
            if isinstance(grp, PermutationGroup):
                return True
            if isinstance(grp, FreeGroup):
                if hasattr(grp, 'rank'):
                    return grp.rank <= 1
                return len(grp.generators) <= 1
            return True # Default to True (so neg_Q is False) if unknown
            
        acc_H = check_acc(H)
        neg_q = not acc_H
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a surjective group homomorphism",
    "¬Q: H does not satisfy the ascending chain condition on normal subgroups"
]

N_HYP = 2
NEG_Q_INDEX = 2