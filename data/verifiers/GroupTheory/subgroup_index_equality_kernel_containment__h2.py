import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(elements, group):
    if not elements:
        return False
    elements = set(elements)
    
    group_elems = None
    if hasattr(group, 'elements'):
        group_elems = set(group.elements)
    elif isinstance(group, (set, list, tuple)):
        group_elems = set(group)
        
    if group_elems is not None and not elements.issubset(group_elems):
        return False
        
    identity = getattr(group, 'identity', None)
    if identity is None:
        for e in elements:
            try:
                if e*e == e:
                    identity = e
                    break
            except Exception:
                pass
        else:
            return False
            
    if identity not in elements:
        return False
        
    for x in elements:
        try:
            inv = x**-1
        except Exception:
            inv = None
            for y in elements:
                try:
                    if x*y == identity and y*x == identity:
                        inv = y
                        break
                except Exception:
                    pass
            if inv is None:
                return False
                
        if inv not in elements:
            return False
            
        for y in elements:
            try:
                if x*y not in elements:
                    return False
            except Exception:
                return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            A = witness.get('A')
            B = witness.get('B')
            f = witness.get('f')
        else:
            G, H, A, B, f = witness
    except Exception:
        return [False, False, False, False]

    def get_elements(obj):
        if hasattr(obj, 'elements'):
            return set(obj.elements)
        return set(obj)

    # H1: G and H are groups
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        h1 = is_subgroup(G_elems, G) and is_subgroup(H_elems, H)
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G such that A is a subset of B
    try:
        A_elems = get_elements(A)
        B_elems = get_elements(B)
        G_elems = get_elements(G)
        h2 = is_subgroup(A_elems, G) and is_subgroup(B_elems, G) and \
             A_elems.issubset(B_elems) and B_elems.issubset(G_elems)
    except Exception:
        h2 = False

    # H3: The kernel of f is a subgroup of A
    try:
        if isinstance(f, dict):
            func = lambda x: f[x]
        else:
            func = f
            
        H_elems = get_elements(H)
        H_id = getattr(H, 'identity', None)
        if H_id is None:
            for e in H_elems:
                try:
                    if e*e == e:
                        H_id = e
                        break
                except Exception:
                    pass
                    
        G_elems = get_elements(G)
        ker = {x for x in G_elems if func(x) == H_id}
        h3 = is_subgroup(ker, G) and ker.issubset(A_elems)
    except Exception:
        h3 = False

    # neg_Q: The index of A in B is equal to the index of f(A) in f(B)
    try:
        if isinstance(f, dict):
            func = lambda x: f[x]
        else:
            func = f
            
        A_elems = get_elements(A)
        B_elems = get_elements(B)
        
        f_B = {func(x) for x in B_elems}
        f_A = {func(x) for x in A_elems}
        
        if len(A_elems) == 0 or len(f_A) == 0:
            neg_q = True
        elif not is_subgroup(f_B, H) or not is_subgroup(f_A, H):
            neg_q = True
        elif not f_A.issubset(f_B):
            neg_q = True
        else:
            # Check if index of A in B == index of f(A) in f(B)
            # using cross-multiplication to avoid floats
            neg_q = (len(B_elems) * len(f_A) != len(f_B) * len(A_elems))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and B are subgroups of G such that A is a subset of B",
    "H_3: The kernel of f is a subgroup of A",
    "¬Q: The index of A in B is not equal to the index of f(A) in f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3