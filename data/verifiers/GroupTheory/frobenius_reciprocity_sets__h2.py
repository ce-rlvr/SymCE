import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
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
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, Y, action)
    where:
      - G is a group (e.g., a PermutationGroup or list of permutations)
      - H is a subset of G (list of permutations)
      - Y is a set (list of elements)
      - action is a callable action(g, y) returning an element of Y
    """
    try:
        G, H, Y, action = witness
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
        else:
            G_elements = list(G)
            
        if hasattr(H, 'elements'):
            H_elements = list(H.elements)
        else:
            H_elements = list(H)
            
        Y_list = list(Y)
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group acting on a set Y
    try:
        if not G_elements or not Y_list:
            h1_ok = False
        else:
            is_group = True
            id_perm = G_elements[0]**0
            if id_perm not in G_elements:
                is_group = False
            for g1 in G_elements:
                if ~g1 not in G_elements:
                    is_group = False
                    break
                for g2 in G_elements:
                    if g1 * g2 not in G_elements:
                        is_group = False
                        break
                if not is_group:
                    break
                    
            if not is_group:
                h1_ok = False
            else:
                action_ok = True
                for y in Y_list:
                    if action(id_perm, y) != y:
                        action_ok = False
                        break
                    for g1 in G_elements:
                        gy = action(g1, y)
                        if gy not in Y_list:
                            action_ok = False
                            break
                        for g2 in G_elements:
                            if action(g1, action(g2, y)) != action(g1 * g2, y):
                                action_ok = False
                                break
                        if not action_ok:
                            break
                    if not action_ok:
                        break
                h1_ok = action_ok
    except Exception:
        h1_ok = False

    # H_2: H is a subset of G
    try:
        h2_ok = len(H_elements) > 0 and all(h in G_elements for h in H_elements)
    except Exception:
        h2_ok = False

    # neg_Q: The number of G-equivariant maps from G/H to Y is not equal to the size of Y^H
    try:
        # Construct the set of left cosets G/H
        G_mod_H = set()
        for g in G_elements:
            coset = frozenset(g * h for h in H_elements)
            G_mod_H.add(coset)
            
        G_mod_H = list(G_mod_H)
        
        # Find orbits of G acting on G/H by left multiplication
        visited = set()
        orbits = []
        for C in G_mod_H:
            if C not in visited:
                orbit = set()
                for g in G_elements:
                    gC = frozenset(g * x for x in C)
                    orbit.add(gC)
                    visited.add(gC)
                orbits.append(C)
                
        # Count the number of G-equivariant maps
        num_maps = 1
        for C in orbits:
            # Find the stabilizer of the representative C in G
            stab_C = []
            for g in G_elements:
                gC = frozenset(g * x for x in C)
                if gC == C:
                    stab_C.append(g)
                    
            # Count how many elements y in Y are fixed by the stabilizer
            valid_y_count = 0
            for y in Y_list:
                is_valid = True
                for g in stab_C:
                    if action(g, y) != y:
                        is_valid = False
                        break
                if is_valid:
                    valid_y_count += 1
            num_maps *= valid_y_count
            
        # Find the set of fixed points Y^H
        Y_H = []
        for y in Y_list:
            is_fixed = True
            for h in H_elements:
                if action(h, y) != y:
                    is_fixed = False
                    break
            if is_fixed:
                Y_H.append(y)
                
        # The conclusion fails if the sizes do not match
        neg_q_ok = (num_maps != len(Y_H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set Y",
    "H_2: H is a subset of G",
    "¬Q: The number of G-equivariant maps from G/H to Y is not equal to the size of Y^H"
]

N_HYP = 2
NEG_Q_INDEX = 2