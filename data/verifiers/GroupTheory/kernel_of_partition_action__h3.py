import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Parse witness: can be (G, P) or (G, X, P)
    try:
        if len(witness) == 2:
            G, P = witness
            X = set(range(G.degree))
        elif len(witness) == 3:
            G, X, P = witness
            X = set(X)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            # Check if X is invariant under G (i.e., G acts on X)
            for g in G.generators:
                if any(g(x) not in X for x in X):
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H_2: P is a partition of X
    try:
        if not h1:
            h2 = False
        else:
            P_sets = [set(b) for b in P]
            if any(not b for b in P_sets):
                h2 = False
            else:
                union = set()
                disjoint = True
                for b in P_sets:
                    if not union.isdisjoint(b):
                        disjoint = False
                        break
                    union.update(b)
                h2 = disjoint and union == X
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails.
    # The conclusion states that the kernel of the induced action of G on P is \bigcap N_G(P_i).
    # This is a definitional tautology IF the induced action exists.
    # The only way the conclusion fails is if the induced action is not well-defined,
    # which happens when G does not preserve the partition P.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            P_sets = [set(b) for b in P]
            acts = True
            for g in G.generators:
                for b in P_sets:
                    img = set(g(x) for x in b)
                    if img not in P_sets:
                        acts = False
                        break
                if not acts:
                    break
            neg_q = not acts
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: P is a partition of X",
    "¬Q: The induced action of G on P is not well-defined (G does not preserve P)"
]

N_HYP = 2
NEG_Q_INDEX = 2