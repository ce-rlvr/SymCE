import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        X = witness['X']
        R = witness['R']
        f = witness['f']
    except Exception:
        return [False, False, False, False]
        
    # H_1: H is a group
    try:
        elements_H = list(H.elements)
        id_H = elements_H[0]**0
        h1 = hasattr(H, 'elements') and hasattr(H, 'generators')
    except Exception:
        h1 = False

    # H_2: f: X -> H is a map of sets
    try:
        h2 = isinstance(f, dict) and all(x in X for x in f.keys()) and all(x in f for x in X) and all(v in elements_H for v in f.values())
    except Exception:
        h2 = False

    # H_3: For every word r in R, substitution yields identity in H
    try:
        h3 = True
        for r in R:
            val = id_H
            for x in r:
                if x in f:
                    val = val * f[x]
                elif x**-1 in f:
                    val = val * (f[x**-1]**-1)
                else:
                    h3 = False
                    break
            if not h3:
                break
            if val != id_H:
                h3 = False
                break
    except Exception:
        h3 = False

    # neg_Q: There does not exist a unique homomorphism phi: G -> H extending f
    try:
        elements_G = list(G.elements)
        id_G = elements_G[0]**0
        
        gens = G.generators if hasattr(G, 'generators') else elements_G
        
        valid_homs = 0
        
        possible_values = [elements_H for _ in gens]
        
        for h_tuple in itertools.product(*possible_values):
            phi = {id_G: id_H}
            queue = [id_G]
            gen_map = dict(zip(gens, h_tuple))
            
            is_hom = True
            idx = 0
            while idx < len(queue):
                curr = queue[idx]
                idx += 1
                for g in gens:
                    nxt = curr * g
                    val = phi[curr] * gen_map[g]
                    if nxt in phi:
                        if phi[nxt] != val:
                            is_hom = False
                            break
                    else:
                        phi[nxt] = val
                        queue.append(nxt)
                if not is_hom:
                    break
                    
            if is_hom and len(phi) == len(elements_G):
                matches_f = True
                for x in X:
                    if phi.get(x) != f[x]:
                        matches_f = False
                        break
                if matches_f:
                    valid_homs += 1
                    if valid_homs > 1:
                        break
                        
        neg_q = (valid_homs != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: f: X -> H is a map of sets",
    "H_3: For every word r in R, substitution yields identity in H",
    "¬Q: There does not exist a unique homomorphism phi: G -> H extending f"
]

N_HYP = 3
NEG_Q_INDEX = 3