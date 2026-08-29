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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
        G, x = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts on itself by conjugation
    # This is a universal property of groups. We just verify x is a valid subset/element in G.
    try:
        if isinstance(x, PermutationGroup):
            h2 = h1 and x.is_subgroup(G)
        elif isinstance(x, (list, set, tuple)):
            h2 = h1 and all(y in list(G.elements) for y in x)
        else:
            h2 = h1 and x in list(G.elements)
    except Exception:
        h2 = False

    # ¬Q: The stabilizer of x under the conjugation action is NOT equal to the centralizer C_G(x)
    try:
        if isinstance(x, PermutationGroup):
            x_elements = list(x.elements)
        elif isinstance(x, (list, set, tuple)):
            x_elements = list(x)
        else:
            x_elements = [x]

        stab = set()
        cent = set()
        
        x_set = set(x_elements)
        g_elements = list(G.elements)
        
        for g in g_elements:
            # Conjugate all elements in x
            conj_elements = [g * y * ~g for y in x_elements]
            
            # Stabilizer condition: the set of conjugated elements equals the original set
            if set(conj_elements) == x_set:
                stab.add(g)
                
            # Centralizer condition: each element is fixed under conjugation
            if all(conj_elements[i] == x_elements[i] for i in range(len(x_elements))):
                cent.add(g)
                
        neg_q = (stab != cent)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on itself by conjugation",
    "¬Q: The stabilizer of x under the conjugation action is not equal to the centralizer C_G(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2