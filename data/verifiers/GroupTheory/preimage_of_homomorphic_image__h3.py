import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'generate'):
        return list(group.generate())
    elif hasattr(group, 'elements'):
        return list(group.elements)
    else:
        return list(group)

def get_op(elems):
    if not elems:
        return lambda a, b: a * b
    x = elems[0]
    try:
        _ = x * x
        return lambda a, b: a * b
    except Exception:
        return lambda a, b: a + b

def check_group(elems):
    if not elems:
        return False
    op = get_op(elems)
    e = None
    for x in elems:
        try:
            if op(x, x) == x:
                e = x
                break
        except Exception:
            pass
    if e is None:
        return False
    for x in elems:
        inv_found = False
        for y in elems:
            try:
                xy = op(x, y)
            except Exception:
                return False
            if xy not in elems:
                return False
            if xy == e and op(y, x) == e:
                inv_found = True
        if not inv_found:
            return False
    return True

def is_group(G):
    if hasattr(G, 'is_group') and G.is_group:
        return True
    if hasattr(G, 'is_Group') and G.is_Group:
        return True
    try:
        elems = get_elements(G)
        return check_group(elems)
    except Exception:
        return False

def evaluate_phi(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    elif isinstance(phi, (list, tuple)):
        for pair in phi:
            if pair[0] == x:
                return pair[1]
        raise ValueError("Mapping not found")
    else:
        return phi(x)

def conditions(witness):
    try:
        G, H, phi, A = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False
        
    # H_2: phi is a group homomorphism
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        op_G = get_op(G_elems)
        op_H = get_op(H_elems)
        
        h2 = True
        for x in G_elems:
            px = evaluate_phi(phi, x)
            if px not in H_elems:
                h2 = False
                break
        if h2:
            for x in G_elems:
                for y in G_elems:
                    if evaluate_phi(phi, op_G(x, y)) != op_H(evaluate_phi(phi, x), evaluate_phi(phi, y)):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The preimage phi^{-1}(phi(A)) is equal to the product A ker(phi)
    try:
        A_elems = get_elements(A)
        G_elems = get_elements(G)
        op_G = get_op(G_elems)
        
        H_elems = get_elements(H)
        op_H = get_op(H_elems)
        e_H = None
        for y in H_elems:
            if op_H(y, y) == y:
                e_H = y
                break
                
        ker_phi = []
        for x in G_elems:
            if evaluate_phi(phi, x) == e_H:
                ker_phi.append(x)
                
        phi_A = []
        for a in A_elems:
            pa = evaluate_phi(phi, a)
            if pa not in phi_A:
                phi_A.append(pa)
                
        preimage = []
        for x in G_elems:
            if evaluate_phi(phi, x) in phi_A:
                if x not in preimage:
                    preimage.append(x)
                    
        A_ker = []
        for a in A_elems:
            for k in ker_phi:
                prod = op_G(a, k)
                if prod not in A_ker:
                    A_ker.append(prod)
                    
        def is_subset(l1, l2):
            for item in l1:
                if item not in l2:
                    return False
            return True
            
        q = is_subset(preimage, A_ker) and is_subset(A_ker, preimage)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi: G -> H is a group homomorphism",
    "¬Q: The preimage phi^{-1}(phi(A)) is not equal to the product A ker(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2