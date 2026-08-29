import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple: (G, X, B)
        # G: PermutationGroup
        # X: set of non-negative integers
        # B: set of non-negative integers
        G, X, B = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group acting on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif not isinstance(X, (set, list, tuple)):
            h1 = False
        else:
            X_set = set(X)
            h1 = True
            # Check if X is closed under the action of G
            for g in G.generators:
                for x in X_set:
                    if g(x) not in X_set:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: B is a non-empty block of imprimitivity in X
    try:
        B_set = set(B)
        if not h1:
            h2 = False
        elif not B_set.issubset(X_set) or len(B_set) == 0:
            h2 = False
        else:
            h2 = True
            # For any g in G, either g * B = B or (g * B) \cap B = \emptyset
            for g in G.generate():
                gB = {g(x) for x in B_set}
                if gB != B_set and not gB.isdisjoint(B_set):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The set of distinct translates {g * B | g in G} does NOT form a partition of X
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            translates = []
            for g in G.generate():
                gB = frozenset({g(x) for x in B_set})
                if gB not in translates:
                    translates.append(gB)
            
            union_translates = set()
            for t in translates:
                union_translates.update(t)
            
            is_partition = True
            # Condition 1: The union of all translates must equal X
            if union_translates != X_set:
                is_partition = False
            else:
                # Condition 2: Translates must be pairwise disjoint
                for i in range(len(translates)):
                    for j in range(i + 1, len(translates)):
                        if not translates[i].isdisjoint(translates[j]):
                            is_partition = False
                            break
                    if not is_partition:
                        break
                # Condition 3: No empty sets in the partition
                if frozenset() in translates:
                    is_partition = False
                    
            neg_q = not is_partition
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: B is a non-empty block of imprimitivity in X",
    "¬Q: The set of distinct translates {g * B | g in G} does not form a partition of X"
]

N_HYP = 2
NEG_Q_INDEX = 2