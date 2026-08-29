import itertools
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def group_rank(G):
    """
    Computes the rank (minimum number of generators) of a group.
    """
    if hasattr(G, 'rank'):
        r = G.rank
        return r() if callable(r) else r
        
    if hasattr(G, 'order') and callable(G.order):
        try:
            n = G.order()
            if n == 1:
                return 0
            elements = list(G.elements)
            # Check for rank 1 (cyclic)
            for g in elements:
                if PermutationGroup(g).order() == n:
                    return 1
            # Check for rank 2
            for comb in itertools.combinations(elements, 2):
                if PermutationGroup(*comb).order() == n:
                    return 2
            # Check for rank 3
            for comb in itertools.combinations(elements, 3):
                if PermutationGroup(*comb).order() == n:
                    return 3
        except Exception:
            pass
            
    if hasattr(G, 'generators'):
        return len(list(G.generators))
        
    raise ValueError("Cannot compute rank")

def conditions(witness) -> list[bool]:
    try:
        is_ab = bool(witness.is_abelian)
        r = group_rank(witness)
        # The conclusion is: F is abelian <=> rank(F) <= 1
        # We want the negated conclusion (i.e., the biconditional fails)
        neg_q = not (is_ab == (r <= 1))
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: F is an abelian group if and only if the rank of F is at most 1"
]

N_HYP = 0
NEG_Q_INDEX = 0