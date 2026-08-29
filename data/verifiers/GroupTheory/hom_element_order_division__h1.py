import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard groups and matrices
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

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def get_order(x, group_elements=None):
    try:
        if hasattr(x, 'order'):
            ans = x.order() if callable(x.order) else x.order
            if ans is not None:
                return ans
    except Exception:
        pass
    
    try:
        if hasattr(x, 'is_Identity') and x.is_Identity:
            return 1
    except Exception:
        pass

    try:
        curr = x
        for i in range(1, 2000):
            if hasattr(curr, 'is_Identity') and curr.is_Identity:
                return i
            if hasattr(curr, 'is_identity') and curr.is_identity:
                return i
            if hasattr(curr, 'is_Identity_Matrix') and curr.is_Identity_Matrix:
                return i
            if hasattr(curr, 'shape') and curr == sympy.eye(curr.shape[0]):
                return i
            
            if group_elements:
                is_id = True
                for g_test in group_elements:
                    if curr * g_test != g_test:
                        is_id = False
                        break
                if is_id:
                    return i
            
            curr = curr * x
        return float('inf')
    except Exception:
        return float('inf')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, H, phi, g = witness
        elif len(witness) == 2:
            phi, g = witness
            G = phi.domain
            H = phi.codomain
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: phi is a group homomorphism from G to H
    try:
        h1_ok = False
        G_elements = get_elements(G)
        H_elements = get_elements(H)
        
        is_hom = True
        if isinstance(phi, dict):
            for x in G_elements:
                if phi.get(x) not in H_elements:
                    is_hom = False
                    break
            if is_hom:
                for x in G_elements:
                    for y in G_elements:
                        if phi.get(x*y) != phi.get(x)*phi.get(y):
                            is_hom = False
                            break
                    if not is_hom:
                        break
        elif callable(phi):
            for x in G_elements:
                if phi(x) not in H_elements:
                    is_hom = False
                    break
            if is_hom:
                for x in G_elements:
                    for y in G_elements:
                        if phi(x*y) != phi(x)*phi(y):
                            is_hom = False
                            break
                    if not is_hom:
                        break
        else:
            is_hom = False
            
        h1_ok = is_hom
    except Exception:
        h1_ok = False

    # H_2: g in G and has finite order
    try:
        h2_ok = False
        G_elements = get_elements(G)
        if g in G_elements:
            order_g = get_order(g, G_elements)
            if order_g > 0 and order_g != float('inf'):
                h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: order of phi(g) in H is not finite or does not divide order of g
    try:
        neg_q_ok = False
        if isinstance(phi, dict):
            phig = phi.get(g)
        else:
            phig = phi(g)
            
        H_elements = get_elements(H)
        order_phig = get_order(phig, H_elements)
        
        G_elements = get_elements(G)
        order_g = get_order(g, G_elements)
        
        if order_phig == 0 or order_phig == float('inf'):
            neg_q_ok = True
        elif order_g % order_phig != 0:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: g is an element of G of finite order",
    "¬Q: The order of phi(g) in H is not finite or does not divide the order of g"
]

N_HYP = 2
NEG_Q_INDEX = 2