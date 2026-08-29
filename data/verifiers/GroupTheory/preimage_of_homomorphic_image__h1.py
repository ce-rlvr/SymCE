import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup
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
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            phi = witness['phi']
            A = witness['A']
        else:
            G, H, phi, A = witness
    except Exception:
        return [False, False, False]

    def get_elements(obj):
        if hasattr(obj, 'elements'):
            try:
                elems = obj.elements
                if callable(elems):
                    return list(elems())
                return list(elems)
            except Exception:
                pass
        if hasattr(obj, 'generate'):
            try:
                return list(obj.generate())
            except Exception:
                pass
        try:
            return list(obj)
        except TypeError:
            return [obj]

    def apply_phi(phi_map, x):
        if isinstance(phi_map, dict):
            return phi_map[x]
        elif hasattr(phi_map, '__call__'):
            return phi_map(x)
        else:
            for k, v in phi_map:
                if k == x:
                    return v
            raise ValueError("Mapping not found")

    # H_1: phi is a group homomorphism from G to H
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        h1_ok = True
        if not G_elems or not H_elems:
            h1_ok = False
        else:
            for g1 in G_elems:
                p1 = apply_phi(phi, g1)
                if p1 not in H_elems:
                    h1_ok = False
                    break
                for g2 in G_elems:
                    p2 = apply_phi(phi, g2)
                    p12 = apply_phi(phi, g1 * g2)
                    if p12 != p1 * p2:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: A is a subgroup of G
    try:
        A_elems = get_elements(A)
        G_elems = get_elements(G)
        h2_ok = True
        if not A_elems:
            h2_ok = False
        else:
            for a in A_elems:
                if a not in G_elems:
                    h2_ok = False
                    break
            if h2_ok:
                for a1 in A_elems:
                    for a2 in A_elems:
                        if (a1 * a2) not in A_elems:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
            if h2_ok:
                for a in A_elems:
                    if (a**-1) not in A_elems:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False

    # neg_Q: The preimage phi^-1(phi(A)) is not equal to the product A ker(phi)
    try:
        G_elems = get_elements(G)
        A_elems = get_elements(A)
        
        e_G = None
        for g in G_elems:
            if g * g == g:
                e_G = g
                break
                
        if e_G is None:
            neg_q_ok = False
        else:
            e_H = apply_phi(phi, e_G)
            
            phi_A = []
            for a in A_elems:
                pa = apply_phi(phi, a)
                if pa not in phi_A:
                    phi_A.append(pa)
                    
            preimage = []
            for g in G_elems:
                if apply_phi(phi, g) in phi_A:
                    preimage.append(g)
                    
            ker = []
            for g in G_elems:
                if apply_phi(phi, g) == e_H:
                    ker.append(g)
                    
            product_A_ker = []
            for a in A_elems:
                for k in ker:
                    ak = a * k
                    if ak not in product_A_ker:
                        product_A_ker.append(ak)
                        
            def is_subset(l1, l2):
                for x in l1:
                    if x not in l2:
                        return False
                return True
                
            sets_equal = is_subset(preimage, product_A_ker) and is_subset(product_A_ker, preimage)
            neg_q_ok = not sets_equal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: A is a subgroup of G",
    "¬Q: The preimage phi^-1(phi(A)) is not equal to the product A ker(phi)"
]
N_HYP = 2
NEG_Q_INDEX = 2