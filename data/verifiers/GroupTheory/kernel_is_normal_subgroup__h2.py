import itertools
import functools
import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _check_group(G, op_G):
    if not G: 
        return False
    # closure
    for a in G:
        for b in G:
            try:
                c = op_G(a, b)
                if c not in G: 
                    return False
            except Exception:
                return False
    # associativity
    for a in G:
        for b in G:
            for c in G:
                try:
                    if op_G(op_G(a, b), c) != op_G(a, op_G(b, c)): 
                        return False
                except Exception:
                    return False
    # identity
    e = None
    for elem in G:
        try:
            if all(op_G(elem, a) == a and op_G(a, elem) == a for a in G):
                e = elem
                break
        except Exception:
            return False
    if e is None: 
        return False
    # inverses
    for a in G:
        has_inv = False
        for b in G:
            try:
                if op_G(a, b) == e and op_G(b, a) == e:
                    has_inv = True
                    break
            except Exception:
                return False
        if not has_inv: 
            return False
    return True

def _check_hom(G, op_G, H, op_H, phi):
    for a in G:
        try:
            pa = phi(a)
            if pa not in H: 
                return False
        except Exception:
            return False
        for b in G:
            try:
                if phi(op_G(a, b)) != op_H(phi(a), phi(b)): 
                    return False
            except Exception:
                return False
    return True

def _check_neg_q(G, op_G, H, op_H, phi):
    # Find identity of H
    e_H = None
    for elem in H:
        try:
            if all(op_H(elem, a) == a and op_H(a, elem) == a for a in H):
                e_H = elem
                break
        except Exception:
            pass
            
    if e_H is None:
        # If H has no identity, the kernel is mathematically undefined,
        # hence it cannot be a normal subgroup.
        return True
    
    # Compute Kernel
    ker = []
    for g in G:
        try:
            if phi(g) == e_H:
                ker.append(g)
        except Exception:
            return False
            
    if not ker:
        # Empty set is not a subgroup
        return True
    
    # Check if ker is a normal subgroup
    # closure
    for a in ker:
        for b in ker:
            try:
                if op_G(a, b) not in ker: 
                    return True
            except Exception:
                return False
    
    # identity of G
    e_G = None
    for elem in G:
        try:
            if all(op_G(elem, a) == a and op_G(a, elem) == a for a in G):
                e_G = elem
                break
        except Exception:
            pass
    if e_G not in ker: 
        return True
    
    # inverses
    for a in ker:
        inv_a = None
        for b in G:
            try:
                if op_G(a, b) == e_G and op_G(b, a) == e_G:
                    inv_a = b
                    break
            except Exception:
                pass
        if inv_a not in ker: 
            return True
    
    # normality
    for g in G:
        inv_g = None
        for b in G:
            try:
                if op_G(g, b) == e_G and op_G(b, g) == e_G:
                    inv_g = b
                    break
            except Exception:
                pass
        for k in ker:
            try:
                if op_G(g, op_G(k, inv_g)) not in ker:
                    return True
            except Exception:
                return False
                
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = list(witness['G'])
            op_G = witness['op_G']
            H = list(witness['H'])
            op_H = witness['op_H']
            phi = witness['phi']
        elif isinstance(witness, tuple) and len(witness) == 5:
            G, op_G, H, op_H, phi = witness
            G = list(G)
            H = list(H)
        else:
            G = list(witness.G)
            op_G = witness.op_G
            H = list(witness.H)
            op_H = witness.op_H
            phi = witness.phi
    except Exception:
        return [False, False, False]

    try:
        h1_ok = _check_group(G, op_G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = _check_hom(G, op_G, H, op_H, phi)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = _check_neg_q(G, op_G, H, op_H, phi)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The kernel of phi is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2