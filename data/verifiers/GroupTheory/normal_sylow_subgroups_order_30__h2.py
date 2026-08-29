import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: G does NOT have both a unique normal Sylow 3-subgroup and a unique normal Sylow 5-subgroup
    try:
        if not h1:
            neg_q = False
        else:
            P3 = witness.sylow_subgroup(3)
            P5 = witness.sylow_subgroup(5)
            
            def is_normal(G, H):
                for g in G.generators:
                    g_inv = ~g
                    for h in H.generators:
                        if (g * h * g_inv) not in H:
                            return False
                return True
            
            normal_3 = is_normal(witness, P3)
            normal_5 = is_normal(witness, P5)
            
            neg_q = not (normal_3 and normal_5)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G does not have both a unique normal Sylow 3-subgroup and a unique normal Sylow 5-subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1