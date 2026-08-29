import sympy
from sympy.combinatorics import PermutationGroup, AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(G, S):
    """Check if S is a subgroup of G by checking generators."""
    for s in S.generators:
        if s not in G:
            return False
    return True

def is_normal_subgroup(G, S):
    """Check if S is a normal subgroup of G."""
    for g in G.generators:
        for s in S.generators:
            if (g * s * ~g) not in S:
                return False
    return True

def group_eq(G1, G2):
    """Check if two permutation groups are equal."""
    if G1.order() != G2.order():
        return False
    return is_subgroup(G1, G2)

def is_semisimple(G):
    """Check if G is a semisimple group (no non-trivial abelian normal subgroups)."""
    for N in G.normal_subgroups():
        if N.order() == 1:
            continue
        if N.is_abelian:
            return False
    return True

def is_non_abelian_simple_direct_factor(G, S):
    """Check if S is a non-abelian simple group that is a direct factor of G."""
    if S.is_abelian:
        return False
    norms_S = S.normal_subgroups()
    if len(norms_S) != 2:
        return False
    if not is_subgroup(G, S):
        return False
    if not is_normal_subgroup(G, S):
        return False
    
    norms_G = G.normal_subgroups()
    for H in norms_G:
        if S.order() * H.order() == G.order():
            # Since S is simple, if S is not a subgroup of H, their intersection is trivial.
            if not is_subgroup(H, S):
                return True
    return False

def compute_I_S(G, S):
    """Compute the isotypic component of G corresponding to S."""
    min_norms = []
    norms = G.normal_subgroups()
    for N in norms:
        if N.order() == 1:
            continue
        is_minimal = True
        for M in norms:
            if M.order() == 1 or M.order() == N.order():
                continue
            if is_subgroup(N, M):
                is_minimal = False
                break
        if is_minimal:
            if N.order() == S.order():
                try:
                    if N.is_isomorphic(S):
                        min_norms.append(N)
                except Exception:
                    # Fallback if is_isomorphic fails but orders match for simple groups
                    min_norms.append(N)
                    
    if not min_norms:
        return PermutationGroup([Permutation()])
    
    gens = []
    for N in min_norms:
        gens.extend(N.generators)
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if len(witness) == 4:
            G, S, I_S_wit, alpha = witness
        elif len(witness) == 3:
            G, S, alpha = witness
            I_S_wit = None
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G is a semisimple group
    try:
        h2 = is_semisimple(G)
    except Exception:
        h2 = False

    # H3: S is a non-abelian simple group that is a direct factor of G
    try:
        h3 = is_non_abelian_simple_direct_factor(G, S)
    except Exception:
        h3 = False

    # H4: I_S is the isotypic component of G corresponding to S
    try:
        I_S_calc = compute_I_S(G, S)
        if I_S_wit is not None:
            h4 = group_eq(I_S_wit, I_S_calc)
            I_S = I_S_wit
        else:
            h4 = True
            I_S = I_S_calc
    except Exception:
        h4 = False
        I_S = None

    # neg_Q: alpha(I_S) != I_S
    try:
        if I_S is None:
            neg_q = False
        else:
            img_gens = []
            for g in I_S.generators:
                if isinstance(alpha, dict):
                    img_gens.append(alpha[g])
                elif isinstance(alpha, Permutation):
                    img_gens.append(alpha * g * ~alpha)
                else:
                    img_gens.append(alpha(g))
            img_group = PermutationGroup(img_gens)
            neg_q = not group_eq(img_group, I_S)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: S is a non-abelian simple group that is a direct factor of G",
    "H_4: I_S is the isotypic component of G corresponding to S",
    "¬Q: alpha(I_S) != I_S"
]

N_HYP = 4
NEG_Q_INDEX = 4