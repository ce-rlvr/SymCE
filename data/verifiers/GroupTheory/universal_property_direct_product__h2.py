import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G_1, G_2, K, f_1, f_2 = witness
    except Exception:
        return [False, False, False, False]

    def eval_map(f, x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    # H1: G_1, G_2, and K are groups, and f_1, f_2 are well-defined maps
    try:
        h1 = True
        if not (hasattr(G_1, 'elements') and hasattr(G_2, 'elements') and hasattr(K, 'elements')):
            h1 = False
        else:
            K_els = list(K.elements)
            G1_els = list(G_1.elements)
            G2_els = list(G_2.elements)
            
            for x in K_els:
                if eval_map(f_1, x) not in G1_els:
                    h1 = False
                    break
                if eval_map(f_2, x) not in G2_els:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: f_2: K -> G_2 is a group homomorphism
    try:
        h2 = False
        if h1:
            h2 = True
            K_els = list(K.elements)
            for x in K_els:
                for y in K_els:
                    if eval_map(f_2, x * y) != eval_map(f_2, x) * eval_map(f_2, y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: pi_1 and pi_2 are canonical projection homomorphisms
    # This is a definitional property of the direct product setup, so it holds if the groups are valid.
    try:
        h3 = h1
    except Exception:
        h3 = False

    # neg_Q: There does NOT exist a unique group homomorphism f: K -> G_1 x G_2 such that pi_1 o f = f_1 and pi_2 o f = f_2
    try:
        neg_q = False
        if h1:
            # The only possible map f satisfying the projections is f(x) = (f_1(x), f_2(x)).
            # This map is a group homomorphism if and only if both f_1 and f_2 are group homomorphisms.
            is_hom = True
            K_els = list(K.elements)
            for x in K_els:
                for y in K_els:
                    if eval_map(f_1, x * y) != eval_map(f_1, x) * eval_map(f_1, y):
                        is_hom = False
                        break
                    if eval_map(f_2, x * y) != eval_map(f_2, x) * eval_map(f_2, y):
                        is_hom = False
                        break
                if not is_hom:
                    break
            neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G_1, G_2, and K are groups",
    "H_2: f_2: K -> G_2 is a group homomorphism",
    "H_3: pi_1 and pi_2 are canonical projection homomorphisms",
    "¬Q: There does not exist a unique group homomorphism f: K -> G_1 x G_2 such that pi_1 o f = f_1 and pi_2 o f = f_2"
]

N_HYP = 3
NEG_Q_INDEX = 3