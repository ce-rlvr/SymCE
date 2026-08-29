import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, X, B = witness
        elif len(witness) == 2:
            G, B = witness
            X = set(range(G.degree))
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: B is a block of imprimitivity for the action of G on X
    h1_ok = False
    try:
        if isinstance(G, PermutationGroup):
            X_set = set(X)
            B_set = set(B)
            if len(B_set) > 0 and B_set.issubset(X_set):
                # Check if X is invariant under the action of G
                x_invariant = True
                for gen in G.generators:
                    for x in X_set:
                        if gen(x) not in X_set:
                            x_invariant = False
                            break
                    if not x_invariant:
                        break
                
                if x_invariant:
                    # Check the block of imprimitivity condition:
                    # For all g in G, gB == B or gB is disjoint from B
                    is_block = True
                    for g in G.elements:
                        gB = set(g(x) for x in B_set)
                        if gB != B_set and not gB.isdisjoint(B_set):
                            is_block = False
                            break
                    if is_block:
                        h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The cardinality |B| does not divide the cardinality |X|
    neg_q_ok = False
    try:
        X_set = set(X)
        B_set = set(B)
        len_B = len(B_set)
        len_X = len(X_set)
        if len_B > 0 and len_X % len_B != 0:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is a block of imprimitivity for the action of G on X",
    "¬Q: The cardinality |B| does not divide the cardinality |X|"
]

N_HYP = 1
NEG_Q_INDEX = 1