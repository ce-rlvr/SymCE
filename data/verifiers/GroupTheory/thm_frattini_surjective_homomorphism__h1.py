import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

# Top-level setup: named object bindings
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'elements_'):
        return list(G.elements_)
    else:
        return list(G)

def get_identity(G, elements):
    if hasattr(G, 'identity'):
        return G.identity
    for e in elements:
        if e * e == e:
            return e
    return elements[0]

def generate_subgroup(generators):
    closure = set(generators)
    q2 = list(closure)
    while q2:
        x = q2.pop(0)
        for y in list(closure):
            xy = x * y
            if xy not in closure:
                closure.add(xy)
                q2.append(xy)
            yx = y * x
            if yx not in closure:
                closure.add(yx)
                q2.append(yx)
    return frozenset(closure)

def get_frattini(G):
    if hasattr(G, 'frattini_subgroup'):
        res = G.frattini_subgroup()
        if callable(res):
            return set(res())
        return set(res)
        
    elements = get_elements(G)
    if not elements:
        return set()
        
    identity = get_identity(G, elements)
    
    subgroups = {frozenset([identity])}
    queue = [frozenset([identity])]
    
    while queue:
        current = queue.pop(0)
        for g in elements:
            if g not in current:
                new_gens = current | {g}
                new_sub = generate_subgroup(new_gens)
                if new_sub not in subgroups:
                    subgroups.add(new_sub)
                    queue.append(new_sub)
                    
    proper = [s for s in subgroups if len(s) < len(elements)]
    maximal = []
    for s in proper:
        is_max = True
        for other in proper:
            if s != other and s.issubset(other):
                is_max = False
                break
        if is_max:
            maximal.append(s)
            
    if not maximal:
        return set(elements)
        
    frattini = set(maximal[0])
    for s in maximal[1:]:
        frattini = frattini.intersection(s)
        
    return frattini

def eval_phi(phi, g):
    if isinstance(phi, dict):
        return phi[g]
    else:
        return phi(g)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False]
        
    # H_1: phi is a surjective group homomorphism
    try:
        if hasattr(phi, 'is_surjective'):
            if callable(phi.is_surjective):
                h1_ok = bool(phi.is_surjective())
            else:
                h1_ok = bool(phi.is_surjective)
            if hasattr(phi, 'is_homomorphism'):
                if callable(phi.is_homomorphism):
                    h1_ok = h1_ok and bool(phi.is_homomorphism())
                else:
                    h1_ok = h1_ok and bool(phi.is_homomorphism)
        else:
            elements_G = get_elements(G)
            elements_H = get_elements(H)
            
            is_homo = True
            for g1 in elements_G:
                for g2 in elements_G:
                    if eval_phi(phi, g1) * eval_phi(phi, g2) != eval_phi(phi, g1 * g2):
                        is_homo = False
                        break
                if not is_homo:
                    break
                    
            if not is_homo:
                h1_ok = False
            else:
                image = set(eval_phi(phi, g) for g in elements_G)
                h1_ok = (image == set(elements_H))
    except Exception:
        h1_ok = False
        
    # neg_Q: phi(Phi(G)) is NOT contained in Phi(H)
    try:
        phi_G = get_frattini(G)
        phi_H = get_frattini(H)
        
        image_phi_G = set(eval_phi(phi, g) for g in phi_G)
        
        neg_q_ok = not image_phi_G.issubset(phi_H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a surjective group homomorphism from G to H",
    "¬Q: phi(Phi(G)) is not contained in Phi(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1