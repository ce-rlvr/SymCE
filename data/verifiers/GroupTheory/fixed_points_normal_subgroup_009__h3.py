import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = DihedralGroup(2)  # Klein four-group
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
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            N = witness.get('N')
            action = witness.get('action')
            X_N_witness = witness.get('X_N', None)
        else:
            if len(witness) == 4:
                G, X, N, action = witness
                X_N_witness = None
            elif len(witness) == 5:
                G, X, N, action, X_N_witness = witness
            else:
                return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    def apply_action(g, x):
        if callable(action):
            return action(g, x)
        else:
            return action[(g, x)]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple)) and len(X) > 0
        X_list = list(X)
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        h3 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h3 = False

    # H4: X^N is the set of points in X fixed by every element of N
    try:
        h4 = True
        if not (h1 and h2):
            h4 = False
        else:
            # Verify the action is a well-defined map from G x X to X
            for g in G.elements:
                for x in X_list:
                    res = apply_action(g, x)
                    if res not in X_list:
                        h4 = False
                        break
                if not h4:
                    break
            
            if h4:
                X_N_computed = []
                for x in X_list:
                    fixed = True
                    for n in N.elements:
                        if apply_action(n, x) != x:
                            fixed = False
                            break
                    if fixed:
                        X_N_computed.append(x)
                
                if X_N_witness is not None:
                    h4 = (len(X_N_witness) == len(X_N_computed)) and all(x in X_N_computed for x in X_N_witness)
                    X_N = list(X_N_witness)
                else:
                    X_N = X_N_computed
    except Exception:
        h4 = False

    # neg_Q: The set X^N is not invariant under the action of G
    try:
        if not (h1 and h2 and h4):
            neg_q = False
        else:
            invariant = True
            for g in G.elements:
                for x in X_N:
                    if apply_action(g, x) not in X_N:
                        invariant = False
                        break
                if not invariant:
                    break
            neg_q = not invariant
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: N is a normal subgroup of G",
    "H_4: X^N is the set of points in X fixed by every element of N",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 4
NEG_Q_INDEX = 4