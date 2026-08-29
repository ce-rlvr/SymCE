import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: S is a non-abelian simple group that is a direct factor of G",
    "H_4: alpha is an automorphism of G",
    "¬Q: alpha(I_S) != I_S"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, S, alpha), checks if it is a valid counterexample.
    G: PermutationGroup
    S: PermutationGroup (a subgroup of G)
    alpha: dict or callable representing an automorphism of G
    """
    try:
        G, S, alpha = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: G is a semisimple group (has no non-trivial abelian normal subgroups)
    try:
        h2 = True
        if h1:
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: S is a non-abelian simple group that is a direct factor of G
    try:
        h3 = False
        if h1 and isinstance(S, PermutationGroup):
            # Check if S is non-abelian and simple
            if not S.is_abelian and len(S.normal_subgroups()) == 2:
                # Check if S is a normal subgroup of G
                if S.is_subgroup(G):
                    is_normal = True
                    for g in G.generators:
                        for s in S.generators:
                            if not S.contains(~g * s * g):
                                is_normal = False
                                break
                        if not is_normal: 
                            break
                    
                    if is_normal:
                        # Check if there exists a normal complement K such that G = S x K
                        for K in G.normal_subgroups():
                            if S.order() * K.order() == G.order():
                                # Check if intersection is trivial
                                is_trivial = True
                                for s in S.generators:
                                    if not s.is_Identity and K.contains(s):
                                        is_trivial = False
                                        break
                                if is_trivial:
                                    h3 = True
                                    break
    except Exception:
        h3 = False

    # H_4: alpha is an automorphism of G
    try:
        h4 = False
        if h1:
            elements = list(G.generate())
            mapped = set()
            is_hom = True
            for g in elements:
                ag = alpha(g) if callable(alpha) else alpha.get(g)
                if ag is None or not G.contains(ag):
                    is_hom = False
                    break
                mapped.add(ag)
            
            if is_hom and len(mapped) == len(elements):
                # Check homomorphism property on generators
                for g1 in G.generators:
                    for g2 in G.generators:
                        ag1 = alpha(g1) if callable(alpha) else alpha[g1]
                        ag2 = alpha(g2) if callable(alpha) else alpha[g2]
                        ag12 = alpha(g1 * g2) if callable(alpha) else alpha[g1 * g2]
                        if ag12 != ag1 * ag2:
                            is_hom = False
                            break
                    if not is_hom: 
                        break
                h4 = is_hom
    except Exception:
        h4 = False

    # neg_Q: alpha(I_S) != I_S
    try:
        neg_q = False
        if h1 and h3 and h4:
            isotypic_gens = []
            # Find all direct factors of G isomorphic to S
            for N in G.normal_subgroups():
                if N.order() == S.order() and not N.is_abelian and len(N.normal_subgroups()) == 2:
                    is_direct_factor = False
                    for K in G.normal_subgroups():
                        if N.order() * K.order() == G.order():
                            is_trivial = True
                            for n in N.generators:
                                if not n.is_Identity and K.contains(n):
                                    is_trivial = False
                                    break
                            if is_trivial:
                                is_direct_factor = True
                                break
                    if is_direct_factor:
                        isotypic_gens.extend(N.generators)
            
            if isotypic_gens:
                I_S = PermutationGroup(isotypic_gens)
                alpha_I_S_eq_I_S = True
                for gen in I_S.generators:
                    agen = alpha(gen) if callable(alpha) else alpha[gen]
                    if not I_S.contains(agen):
                        alpha_I_S_eq_I_S = False
                        break
                neg_q = not alpha_I_S_eq_I_S
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]