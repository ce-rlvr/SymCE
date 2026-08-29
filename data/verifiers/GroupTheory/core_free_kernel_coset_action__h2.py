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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: index of H in G is n for some integer n > 0
    try:
        if not h1:
            h2 = False
        else:
            G_elements = list(G.elements)
            H_set = set(H)
            if not H_set.issubset(set(G_elements)):
                h2 = False
            else:
                cosets = set()
                for g in G_elements:
                    coset = frozenset(g * h for h in H_set)
                    cosets.add(coset)
                n = len(cosets)
                h2 = n > 0
    except Exception:
        h2 = False

    # H_3: G acts on the set of left cosets G/H by left multiplication
    try:
        if not h2:
            h3 = False
        else:
            acts = True
            for g in G_elements:
                for C in cosets:
                    gC = frozenset(g * c for c in C)
                    if gC not in cosets:
                        acts = False
                        break
                if not acts:
                    break
            h3 = acts
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            # Kernel of the action
            K_act = set()
            for g in G_elements:
                fixes_all = True
                for C in cosets:
                    gC = frozenset(g * c for c in C)
                    if gC != C:
                        fixes_all = False
                        break
                if fixes_all:
                    K_act.add(g)
            
            # Intersection of conjugates of H
            K_int = set(G_elements)
            for g in G_elements:
                gHg_inv = set(g * h * ~g for h in H_set)
                K_int = K_int.intersection(gHg_inv)
            
            # The conclusion holds iff K_act == K_int
            neg_q = (K_act != K_int)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: index of H in G is n for some integer n > 0",
    "H_3: G acts on the set of left cosets G/H by left multiplication",
    "not Q: The kernel of the action is not the intersection of conjugates of H"
]

N_HYP = 3
NEG_Q_INDEX = 3