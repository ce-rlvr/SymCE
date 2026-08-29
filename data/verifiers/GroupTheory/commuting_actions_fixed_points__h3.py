import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = max(G.degree, H.degree)
            
            # Find the set of fixed points X^H
            X_H = set()
            for x in range(n):
                if all(h(x) == x for h in H.generators):
                    X_H.add(x)
            
            # Check if X^H is invariant under the action of G
            invariant = True
            for x in X_H:
                for g in G.generators:
                    if g(x) not in X_H:
                        invariant = False
                        break
                if not invariant:
                    break
            
            # neg_Q is True if the conclusion FAILS (i.e., X^H is NOT invariant)
            neg_q = not invariant
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a group acting on the set X",
    "¬Q: The set of fixed points X^H is not invariant under the action of G"
]

N_HYP = 2
NEG_Q_INDEX = 2