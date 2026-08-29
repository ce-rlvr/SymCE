import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: G and H are groups",
    "H_3: beta: F -> H is a group homomorphism",
    "not Q: There is no group homomorphism gamma: F -> G such that alpha o gamma = beta"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            F_rank = witness.get('F_rank')
            G = witness.get('G')
            H = witness.get('H')
            alpha = witness.get('alpha')
            beta = witness.get('beta')
        else:
            F, G, H, alpha, beta = witness
            F_rank = None
    except Exception:
        return [False, False, False, False]

    # H1: F is a free group
    try:
        from sympy.combinatorics import FreeGroup
        if isinstance(F, FreeGroup):
            h1 = True
            rank = len(F.generators)
        elif isinstance(F_rank, int) and F_rank >= 0:
            h1 = True
            rank = F_rank
        elif isinstance(F, int) and F >= 0:
            h1 = True
            rank = F
        elif isinstance(F, PermutationGroup) and F.order() == 1:
            h1 = True
            rank = 0
        else:
            h1 = False
            rank = 0
    except Exception:
        h1 = False
        rank = 0

    # H2: G and H are groups
    try:
        h2 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H3: beta: F -> H is a group homomorphism
    try:
        if isinstance(beta, (list, tuple)):
            h3 = len(beta) == rank and all(b in H for b in beta)
            beta_vals = list(beta)
        elif isinstance(beta, dict):
            h3 = len(beta) == rank and all(b in H for b in beta.values())
            beta_vals = list(beta.values())
        elif callable(beta):
            from sympy.combinatorics import FreeGroup
            if isinstance(F, FreeGroup):
                beta_vals = [beta(g) for g in F.generators]
                h3 = all(b in H for b in beta_vals)
            else:
                h3 = False
                beta_vals = []
        else:
            h3 = False
            beta_vals = []
    except Exception:
        h3 = False
        beta_vals = []

    # neg_Q: There is NO gamma: F -> G such that alpha o gamma = beta
    try:
        def eval_alpha(g):
            if isinstance(alpha, dict):
                return alpha.get(g)
            return alpha(g)
        
        gamma_exists = True
        for b in beta_vals:
            b_in_image = False
            for g in G.elements:
                if eval_alpha(g) == b:
                    b_in_image = True
                    break
            if not b_in_image:
                gamma_exists = False
                break
        
        neg_q = not gamma_exists
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]