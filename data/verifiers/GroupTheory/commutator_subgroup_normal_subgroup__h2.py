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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of H and N is not a subgroup of N"
]

def check_subgroup(sub, supergroup):
    try:
        return all(g in supergroup for g in sub.generators)
    except Exception:
        return False

def check_normal(N, G):
    try:
        for g in G.generators:
            for n in N.generators:
                if (g * n * ~g) not in N:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    G, H, N = None, None, None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            N = witness.get('N')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            G, H, N = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and check_subgroup(N, G) and check_normal(N, G)
    except Exception:
        h2 = False

    # neg_Q: [H, N] is not a subgroup of N
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(N, PermutationGroup):
            neg_q = False
        else:
            not_in_N = False
            for h in H.elements:
                for n in N.elements:
                    if (h * n * ~h * ~n) not in N:
                        not_in_N = True
                        break
                if not_in_N:
                    break
            
            neg_q = not_in_N
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]