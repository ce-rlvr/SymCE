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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(G):
    return isinstance(G, PermutationGroup) or type(G).__name__ in ('FpGroup', 'FreeGroup')

def is_free_group(G):
    if type(G).__name__ == 'FreeGroup':
        return True
    if type(G).__name__ == 'FpGroup':
        return len(G.relators) == 0
    if isinstance(G, PermutationGroup):
        return G.order() == 1
    return False

def rank_of_free_group(G):
    if type(G).__name__ == 'FreeGroup':
        return len(G.generators)
    if type(G).__name__ == 'FpGroup' and len(G.relators) == 0:
        return len(G.generators)
    if isinstance(G, PermutationGroup) and G.order() == 1:
        return 0
    return None

def is_free_product(family, F):
    family = list(family)
    if len(family) == 0:
        return is_free_group(F) and rank_of_free_group(F) == 0
        
    if len(family) == 1:
        G = family[0]
        if F == G:
            return True
        if is_free_group(F) and is_free_group(G):
            return rank_of_free_group(F) == rank_of_free_group(G)
        if isinstance(F, PermutationGroup) and isinstance(G, PermutationGroup):
            try:
                return F.is_isomorphic(G)
            except Exception:
                return False
            
    # If all groups are free, the free product is a free group with rank = sum of ranks
    ranks = [rank_of_free_group(G) for G in family]
    if all(r is not None for r in ranks):
        expected_rank = sum(ranks)
        F_rank = rank_of_free_group(F)
        if F_rank is not None:
            return F_rank == expected_rank
            
    # Structural check for FpGroup
    if type(F).__name__ == 'FpGroup':
        expected_gen_count = 0
        expected_rel_count = 0
        for G in family:
            if type(G).__name__ == 'FreeGroup':
                expected_gen_count += len(G.generators)
            elif type(G).__name__ == 'FpGroup':
                expected_gen_count += len(G.generators)
                expected_rel_count += len(G.relators)
            elif isinstance(G, PermutationGroup):
                if G.order() == 1:
                    pass
                else:
                    return False
            else:
                return False
        return len(F.generators) == expected_gen_count and len(F.relators) == expected_rel_count
        
    # Structural check for FreeGroup
    if type(F).__name__ == 'FreeGroup':
        expected_gen_count = 0
        expected_rel_count = 0
        for G in family:
            if type(G).__name__ == 'FreeGroup':
                expected_gen_count += len(G.generators)
            elif type(G).__name__ == 'FpGroup':
                expected_gen_count += len(G.generators)
                expected_rel_count += len(G.relators)
            elif isinstance(G, PermutationGroup):
                if G.order() == 1:
                    pass
                else:
                    return False
            else:
                return False
        return len(F.generators) == expected_gen_count and expected_rel_count == 0

    return False

def conditions(witness):
    try:
        family, F = witness
        family = list(family)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(family, (list, tuple, set)) and all(is_group(G) for G in family)
    except Exception:
        h1 = False
        
    try:
        h2 = all(is_free_group(G) for G in family)
    except Exception:
        h2 = False
        
    try:
        h3 = is_free_product(family, F)
    except Exception:
        h3 = False
        
    try:
        neg_q = not is_free_group(F)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: {F_i} is a family of groups",
    "H_2: For every i in I, F_i is a free group",
    "H_3: F is the free product of the groups {F_i}",
    "¬Q: F is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3