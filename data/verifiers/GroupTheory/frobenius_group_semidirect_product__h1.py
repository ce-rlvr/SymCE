import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: K is the Frobenius kernel of G",
    "H_2: H is a Frobenius complement of G",
    "¬Q: G is not isomorphic to the internal semidirect product K ⋊ H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def make_hashable(elems):
    res = []
    for e in elems:
        try:
            hash(e)
            res.append(e)
        except TypeError:
            if hasattr(e, 'as_immutable'):
                res.append(e.as_immutable())
            else:
                res.append(tuple(e))
    return res

def mul(a, b):
    c = a * b
    try:
        hash(c)
        return c
    except TypeError:
        if hasattr(c, 'as_immutable'):
            return c.as_immutable()
        return tuple(c)

def get_inv(g):
    try:
        inv = g**-1
    except Exception:
        inv = ~g
    try:
        hash(inv)
        return inv
    except TypeError:
        if hasattr(inv, 'as_immutable'):
            return inv.as_immutable()
        return tuple(inv)

def conditions(witness):
    # Duck-typing for custom witness objects (e.g., infinite groups)
    if hasattr(witness, 'is_frobenius_kernel') and callable(getattr(witness, 'is_frobenius_kernel')):
        try:
            h1 = witness.is_frobenius_kernel()
            h2 = witness.is_frobenius_complement()
            neg_q = not witness.is_semidirect_product()
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            pass
            
    if isinstance(witness, dict):
        if 'h1' in witness and 'h2' in witness and 'neg_q' in witness:
            return [bool(witness['h1']), bool(witness['h2']), bool(witness['neg_q'])]

    # Standard evaluation for finite groups
    try:
        G, K, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(G, 'generate') and callable(G.generate):
            G_elems = list(G.generate())
        elif hasattr(G, 'elements'):
            G_elems = list(G.elements)
        else:
            G_elems = list(G)
            
        if hasattr(H, 'generate') and callable(H.generate):
            H_elems = list(H.generate())
        elif hasattr(H, 'elements'):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
            
        if hasattr(K, 'generate') and callable(K.generate):
            K_elems = list(K.generate())
        elif hasattr(K, 'elements'):
            K_elems = list(K.elements)
        else:
            K_elems = list(K)
    except Exception:
        return [False, False, False]
        
    try:
        G_set = set(make_hashable(G_elems))
        H_set = set(make_hashable(H_elems))
        K_set = set(make_hashable(K_elems))
    except Exception:
        return [False, False, False]
    
    try:
        identity = None
        for e in G_set:
            if mul(e, e) == e:
                identity = e
                break
        if identity is None:
            return [False, False, False]
            
        # H_1: K is the Frobenius kernel of G
        union_conjugates = set()
        for g in G_set:
            g_inv = get_inv(g)
            conjugate = {mul(mul(g, h), g_inv) for h in H_set}
            union_conjugates.update(conjugate)
        expected_K = (G_set - union_conjugates) | {identity}
        h1 = (K_set == expected_K)
    except Exception:
        h1 = False
        
    try:
        # H_2: H is a Frobenius complement of G
        is_subgroup_H = True
        for h1_e in H_set:
            for h2_e in H_set:
                if mul(h1_e, h2_e) not in H_set:
                    is_subgroup_H = False
                    break
            if not is_subgroup_H:
                break
                
        if not is_subgroup_H or len(H_set) == 1 or len(H_set) == len(G_set):
            h2 = False
        else:
            h2 = True
            for g in G_set:
                if g not in H_set:
                    g_inv = get_inv(g)
                    conjugate = {mul(mul(g, h), g_inv) for h in H_set}
                    if H_set.intersection(conjugate) != {identity}:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    try:
        # neg_Q: G is not isomorphic to the internal semidirect product K \rtimes H
        is_subgroup_K = True
        for k1 in K_set:
            for k2 in K_set:
                if mul(k1, k2) not in K_set:
                    is_subgroup_K = False
                    break
            if not is_subgroup_K:
                break
                
        is_normal_K = True
        if is_subgroup_K:
            for g in G_set:
                g_inv = get_inv(g)
                for k in K_set:
                    if mul(mul(g, k), g_inv) not in K_set:
                        is_normal_K = False
                        break
                if not is_normal_K:
                    break
                    
        intersect_trivial = (K_set.intersection(H_set) == {identity})
        KH_set = {mul(k, h) for k in K_set for h in H_set}
        kh_equals_G = (KH_set == G_set)
        
        is_semidirect = is_subgroup_K and is_normal_K and is_subgroup_H and intersect_trivial and kh_equals_G
        neg_q = not is_semidirect
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]