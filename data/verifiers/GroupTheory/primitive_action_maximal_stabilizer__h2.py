import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

def conditions(witness):
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts transitively on X
    try:
        h2 = bool(witness.is_transitive())
    except Exception:
        h2 = False

    # ¬Q: The action is primitive XOR the stabilizer of any point is a maximal subgroup
    try:
        # Evaluate primitivity
        # A transitive action is primitive if it preserves no non-trivial partitions.
        # For |X| = 1, the only partition is trivial, so it is primitive.
        # SymPy's is_primitive() returns False for degree 1, so we handle it explicitly.
        if witness.degree == 1:
            is_prim = True
        else:
            is_prim = bool(witness.is_primitive())

        # Evaluate if the stabilizer of a point is a maximal subgroup
        stab = witness.stabilizer(0)
        
        def is_maximal(G, H):
            if G.order() == H.order():
                return False
            # Check if there is any proper subgroup strictly containing H
            for g in G.generate():
                if g not in H:
                    gens = list(H.generators) + [g]
                    K = PermutationGroup(gens)
                    if K.order() < G.order():
                        return False
            return True

        is_max = is_maximal(witness, stab)
        
        # The conclusion is "primitive iff maximal". 
        # The negated conclusion is True when they are not equivalent.
        neg_q = (is_prim != is_max)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "¬Q: The action is primitive XOR the stabilizer of any point is a maximal subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2