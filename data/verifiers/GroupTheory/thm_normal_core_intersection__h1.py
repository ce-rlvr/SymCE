import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(obj):
    elems = []
    limit = 1000
    
    if hasattr(obj, 'elements'):
        try:
            it = obj.elements() if callable(obj.elements) else obj.elements
            for i, x in enumerate(it):
                if i >= limit: break
                elems.append(x)
            return elems
        except Exception:
            pass
            
    if hasattr(obj, 'generate') and callable(obj.generate):
        try:
            for i, x in enumerate(obj.generate()):
                if i >= limit: break
                elems.append(x)
            return elems
        except Exception:
            pass
            
    try:
        for i, x in enumerate(obj):
            if i >= limit: break
            elems.append(x)
        return elems
    except Exception:
        return [obj]

def intersect_lists(list1, list2):
    res = []
    for x in list1:
        if any(x == y for y in list2):
            res.append(x)
    return res

def is_subset(list1, list2):
    for x in list1:
        if not any(x == y for y in list2):
            return False
    return True

def remove_duplicates(lst):
    res = []
    for x in lst:
        if not any(x == y for y in res):
            res.append(x)
    return res

def check_H1(witness):
    try:
        G, H = witness
        G_elems = remove_duplicates(get_elements(G))
        H_elems = remove_duplicates(get_elements(H))
        
        if not is_subset(H_elems, G_elems):
            return False
        if len(H_elems) == 0 or len(G_elems) == 0:
            return False
            
        for a in G_elems:
            for b in G_elems:
                ab = a * b
                if not any(ab == x for x in G_elems):
                    return False
                    
        has_G_identity = False
        G_identity = None
        for e in G_elems:
            is_id = True
            for a in G_elems:
                if not (e * a == a and a * e == a):
                    is_id = False
                    break
            if is_id:
                has_G_identity = True
                G_identity = e
                break
        if not has_G_identity:
            return False
            
        for a in G_elems:
            has_inv = False
            for b in G_elems:
                if a * b == G_identity and b * a == G_identity:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        for a in H_elems:
            for b in H_elems:
                ab = a * b
                if not any(ab == x for x in H_elems):
                    return False
                    
        has_H_identity = False
        H_identity = None
        for e in H_elems:
            is_id = True
            for a in H_elems:
                if not (e * a == a and a * e == a):
                    is_id = False
                    break
            if is_id:
                has_H_identity = True
                H_identity = e
                break
        if not has_H_identity:
            return False
            
        for a in H_elems:
            has_inv = False
            for b in H_elems:
                if a * b == H_identity and b * a == H_identity:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        return True
    except Exception:
        return False

def check_Q(witness):
    try:
        G, H = witness
        G_elems = remove_duplicates(get_elements(G))
        H_elems = remove_duplicates(get_elements(H))
        
        G_identity = None
        for e in G_elems:
            is_id = True
            for a in G_elems:
                if not (e * a == a and a * e == a):
                    is_id = False
                    break
            if is_id:
                G_identity = e
                break
        if G_identity is None:
            return False
            
        def get_inverse(g):
            try:
                inv = ~g
                if any(inv == x for x in G_elems): return inv
            except Exception: pass
            try:
                inv = g.inv()
                if any(inv == x for x in G_elems): return inv
            except Exception: pass
            for x in G_elems:
                if g * x == G_identity and x * g == G_identity:
                    return x
            raise ValueError("No inverse")

        core_elems = list(H_elems)
        for g in G_elems:
            g_inv = get_inverse(g)
            conj = []
            for h in H_elems:
                conj.append(g * h * g_inv)
            core_elems = intersect_lists(core_elems, conj)
            
        if len(core_elems) == 0:
            return False
            
        for a in core_elems:
            for b in core_elems:
                ab = a * b
                if not any(ab == x for x in core_elems):
                    return False
                    
        has_identity = False
        identity = None
        for e in core_elems:
            is_id = True
            for a in core_elems:
                if not (e * a == a and a * e == a):
                    is_id = False
                    break
            if is_id:
                has_identity = True
                identity = e
                break
        if not has_identity:
            return False
            
        for a in core_elems:
            has_inv = False
            for b in core_elems:
                if a * b == identity and b * a == identity:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        for g in G_elems:
            g_inv = get_inverse(g)
            for n in core_elems:
                gn_ginv = g * n * g_inv
                if not any(gn_ginv == x for x in core_elems):
                    return False
                    
        if not is_subset(core_elems, H_elems):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    H1_ok = check_H1(witness)
    Q_ok = check_Q(witness)
    return [H1_ok, not Q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: The intersection of conjugates is not the largest normal subgroup of G contained in H"
]

N_HYP = 1
NEG_Q_INDEX = 1