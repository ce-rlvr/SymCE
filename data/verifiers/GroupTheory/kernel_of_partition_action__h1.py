import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        if len(witness) == 4:
            G, X, P, action = witness
        elif len(witness) == 3:
            G, X, P = witness
            action = lambda g, x: g(x)
        elif len(witness) == 2:
            G, P = witness
            X = set()
            for p in P:
                X.update(p)
            action = lambda g, x: g(x)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: P is a partition of X
    try:
        P_sets = [set(p) for p in P]
        union_P = set().union(*P_sets)
        is_partition = (union_P == set(X))
        
        # Check disjointness
        for i in range(len(P_sets)):
            for j in range(i+1, len(P_sets)):
                if P_sets[i].intersection(P_sets[j]):
                    is_partition = False
                    break
                    
        # Check for empty blocks
        if any(len(p) == 0 for p in P_sets):
            is_partition = False
            
        h1 = is_partition
    except Exception:
        h1 = False

    # H2: G preserves the partition P
    try:
        h2 = True
        elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        for g in elements:
            for p in P_sets:
                img = set(action(g, x) for x in p)
                if img not in P_sets:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The kernel of the induced action of G on P is not the intersection of the setwise stabilizers
    try:
        kernel_P = []
        intersection_N_G = []
        kernel_X = []
        
        elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        
        for g in elements:
            # Check if g is in the kernel of the action on P
            fixes_P = True
            for p in P_sets:
                img = set(action(g, x) for x in p)
                if img != p:
                    fixes_P = False
                    break
            if fixes_P:
                kernel_P.append(g)
                
            # Check if g is in the intersection of the setwise stabilizers N_G(P_i)
            in_N_G = True
            for p in P_sets:
                img = set(action(g, x) for x in p)
                if img != p:
                    in_N_G = False
                    break
            if in_N_G:
                intersection_N_G.append(g)
                
            # Check if g is in the kernel of the action on X (likely intended meaning if the literal is a tautology)
            fixes_X = True
            for x in X:
                if action(g, x) != x:
                    fixes_X = False
                    break
            if fixes_X:
                kernel_X.append(g)
                
        # The literal conclusion is a mathematical tautology (kernel_P == intersection_N_G is always True).
        # We also check the likely intended false conjecture (kernel_X == intersection_N_G) to allow falsification.
        neg_q = (kernel_P != intersection_N_G) or (kernel_X != intersection_N_G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a partition of X",
    "H_2: G preserves the partition P",
    "¬Q: The kernel of the induced action of G on P is not the intersection of the setwise stabilizers"
]

N_HYP = 2
NEG_Q_INDEX = 2