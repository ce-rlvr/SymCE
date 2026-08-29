import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # The witness can be a tuple (G, X) where G is the group and X is the set/subgroup 
        # on which G acts by conjugation. If only G is provided, we assume X = G.elements.
        if isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
        else:
            G = witness
            X = list(G.elements)
            
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            return [False, False]
            
        # Compute the center Z(G)
        center = []
        for g in G.elements:
            is_central = True
            for h in G.generators:
                if g * h * ~g != h:
                    is_central = False
                    break
            if is_central:
                center.append(g)
                
        # Compute the kernel of the conjugation action on X
        kernel = []
        for g in G.elements:
            acts_trivially = True
            if not isinstance(X, (list, tuple, set)):
                X_list = [X]
            else:
                X_list = X
                
            for x in X_list:
                # If x is a subgroup, the action is on the subgroup (kernel is normalizer)
                if hasattr(x, 'generators') and hasattr(x, '__contains__'):
                    for y in x.generators:
                        if g * y * ~g not in x:
                            acts_trivially = False
                            break
                # If x is an element, the action is on the element (kernel is centralizer)
                else:
                    if g * x * ~g != x:
                        acts_trivially = False
                        break
                if not acts_trivially:
                    break
                    
            if acts_trivially:
                kernel.append(g)
                
        # The conclusion states the kernel is exactly Z(G).
        # We negate this for the counterexample.
        neg_q = set(kernel) != set(center)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The kernel of this conjugation action is not exactly the center Z(G) of the group"
]

N_HYP = 1
NEG_Q_INDEX = 1