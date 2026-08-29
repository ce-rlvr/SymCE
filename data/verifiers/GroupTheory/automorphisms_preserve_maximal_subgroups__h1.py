import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def is_maximal_subgroup(G, M):
    try:
        if not isinstance(M, PermutationGroup) or not isinstance(G, PermutationGroup):
            return False
        for g in M.generators:
            if g not in G:
                return False
        if M.order() == G.order():
            return False
        for g in G.elements:
            if g not in M:
                gens = list(M.generators) + [g]
                H = PermutationGroup(gens)
                if H.order() != G.order():
                    return False
        return True
    except Exception:
        return False

def is_automorphism(G, alpha):
    try:
        if not isinstance(G, PermutationGroup):
            return False
        elements = list(G.elements)
        mapped_elements = []
        for g in elements:
            ag = alpha[g] if isinstance(alpha, dict) else alpha(g)
            if ag not in G:
                return False
            mapped_elements.append(ag)
        if len(set(mapped_elements)) != len(elements):
            return False
        for g1 in elements:
            for g2 in elements:
                ag1 = alpha[g1] if isinstance(alpha, dict) else alpha(g1)
                ag2 = alpha[g2] if isinstance(alpha, dict) else alpha(g2)
                ag1g2 = alpha[g1 * g2] if isinstance(alpha, dict) else alpha(g1 * g2)
                if ag1g2 != ag1 * ag2:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, M, alpha = witness
    except Exception:
        return [False, False, False]
    
    h1 = is_maximal_subgroup(G, M)
    h2 = is_automorphism(G, alpha)
    
    try:
        alpha_M_gens = []
        for g in M.generators:
            ag = alpha[g] if isinstance(alpha, dict) else alpha(g)
            alpha_M_gens.append(ag)
        alpha_M = PermutationGroup(alpha_M_gens)
        neg_q = not is_maximal_subgroup(G, alpha_M)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a maximal subgroup of G",
    "H_2: \\alpha is an automorphism of G",
    "¬Q: \\alpha(M) is not a maximal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2