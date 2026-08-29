import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard objects
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: S is a non-abelian simple group",
    "H_3: S is a direct factor of G",
    "H_4: alpha is an automorphism of G",
    "¬Q: alpha(I_S) != I_S"
]

N_HYP = 4
NEG_Q_INDEX = 4

def get_alpha(alpha, g):
    if isinstance(alpha, dict):
        return alpha[g]
    return alpha(g)

def is_iso(G1, G2):
    try:
        if hasattr(G1, 'is_isomorphic'):
            res = G1.is_isomorphic(G2)
            if res is not None:
                return res
    except Exception:
        pass
    if G1.order() != G2.order():
        return False
    if G1.is_abelian != G2.is_abelian:
        return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            S = witness['S']
            alpha = witness['alpha']
        else:
            G, S, alpha = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: S is a non-abelian simple group
    try:
        if not isinstance(S, PermutationGroup):
            h2 = False
        else:
            is_non_abelian = not S.is_abelian
            n_subgroups = S.normal_subgroups()
            is_simple = len(n_subgroups) == 2
            h2 = is_non_abelian and is_simple
    except Exception:
        h2 = False

    # H_3: S is a direct factor of G
    try:
        h3 = False
        if h1 and h2:
            normal_subgroups = G.normal_subgroups()
            N_candidates = [N for N in normal_subgroups if is_iso(N, S)]
            for N in N_candidates:
                for M in normal_subgroups:
                    if N.order() * M.order() == G.order():
                        # Since N is simple, if M does not contain N, their intersection is trivial
                        if any(not M.contains(g) for g in N.generators):
                            h3 = True
                            break
                if h3:
                    break
    except Exception:
        h3 = False

    # H_4: alpha is an automorphism of G
    try:
        h4 = False
        if h1 and (callable(alpha) or isinstance(alpha, dict)):
            elements = list(G.generate())
            image = set()
            is_hom = True
            for g in elements:
                ag = get_alpha(alpha, g)
                if not G.contains(ag):
                    is_hom = False
                    break
                image.add(ag)
            if is_hom and len(image) == len(elements):
                for g in G.generators:
                    ag = get_alpha(alpha, g)
                    for h in elements:
                        ah = get_alpha(alpha, h)
                        agh = get_alpha(alpha, g*h)
                        if agh != ag * ah:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                if is_hom:
                    h4 = True
    except Exception:
        h4 = False

    # ¬Q: alpha(I_S) != I_S
    try:
        neg_Q = False
        if h1 and h2:
            normal_subgroups = G.normal_subgroups()
            # Since S is simple, any normal subgroup isomorphic to S is minimal normal
            min_normal_S = [N for N in normal_subgroups if is_iso(N, S)]
            I_S_gens = []
            for N in min_normal_S:
                I_S_gens.extend(N.generators)
            
            if not I_S_gens:
                neg_Q = False
            else:
                I_S = PermutationGroup(I_S_gens)
                for g in I_S.generators:
                    ag = get_alpha(alpha, g)
                    if not I_S.contains(ag):
                        neg_Q = True
                        break
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, neg_Q]