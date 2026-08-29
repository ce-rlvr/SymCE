import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, X, action, x)
    where:
      - G is a group (e.g., a SymPy PermutationGroup or a custom object)
      - X is a set (e.g., a list, tuple, or set)
      - action is a function action(g, y) defining the group action
      - x is an element (the point whose orbit/stabilizer is being considered)
    """
    try:
        G, X, action, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            elements = list(G.elements)
            identity = G.identity
            h1 = True
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            elements = list(G.elements)
            identity = G.identity
            h1 = True
            
            # Check identity
            for g in elements:
                if g * identity != g or identity * g != g:
                    h1 = False
                    break
                    
            # Check inverses
            if h1:
                for g in elements:
                    has_inverse = False
                    for h in elements:
                        if g * h == identity and h * g == identity:
                            has_inverse = True
                            break
                    if not has_inverse:
                        h1 = False
                        break
                        
            # Check associativity (for small custom groups)
            if h1 and len(elements) <= 50:
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for k in elements:
                            if gh * k != g * (h * k):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        if isinstance(X, (set, frozenset, list, tuple)):
            X_list = list(X)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = True
        if h1 and h2:
            # 1. Identity acts trivially on X
            for y in X_list:
                if action(identity, y) != y:
                    h3 = False
                    break
            # 2. Compatibility on X: g * (h * y) == (g * h) * y
            if h3:
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for y in X_list:
                            if action(g, action(h, y)) != action(gh, y):
                                h3 = False
                                break
                        if not h3: break
                    if not h3: break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The cardinality of the orbit G \cdot x is NOT equal to the index of the stabilizer subgroup G_x in G.
    try:
        if not h1:
            neg_q = False
        else:
            orbit = set()
            for g in elements:
                orbit.add(action(g, x))
            
            stabilizer = []
            for g in elements:
                if action(g, x) == x:
                    stabilizer.append(g)
            
            if len(stabilizer) == 0:
                # If empty, it's not a subgroup, so the conclusion's premise fails
                neg_q = True
            else:
                # Check if stabilizer is actually a subgroup
                is_subgroup = True
                if identity not in stabilizer:
                    is_subgroup = False
                else:
                    for s1 in stabilizer:
                        for s2 in stabilizer:
                            if (s1 * s2) not in stabilizer:
                                is_subgroup = False
                                break
                        if not is_subgroup: break
                
                if not is_subgroup:
                    # If it's not a subgroup, "index of the stabilizer subgroup" is undefined/false
                    neg_q = True
                else:
                    # Check if |Orbit| != [G : G_x]
                    # Equivalent to: |Orbit| * |G_x| != |G|
                    neg_q = (len(orbit) * len(stabilizer)) != len(elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "¬Q: The cardinality of the orbit G \\cdot x is not equal to the index of the stabilizer subgroup G_x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3