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

def get_elements(grp):
    if hasattr(grp, 'generate_elements'):
        return grp.generate_elements()
    elif hasattr(grp, 'elements'):
        return grp.elements
    else:
        return grp

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1_ok = True
        if hasattr(H, 'is_subgroup') and hasattr(G, 'is_group'):
            h1_ok = H.is_subgroup(G)
        else:
            if hasattr(H, 'generators'):
                for h in H.generators:
                    if h not in G:
                        h1_ok = False
                        break
            else:
                H_elems_check = list(get_elements(H))
                for h in H_elems_check:
                    if h not in G:
                        h1_ok = False
                        break
                if h1_ok:
                    for h1 in H_elems_check:
                        try:
                            h1_inv = ~h1
                        except Exception:
                            h1_inv = h1.inv()
                        if h1_inv not in H_elems_check:
                            h1_ok = False
                            break
                        for h2 in H_elems_check:
                            if (h1 * h2) not in H_elems_check:
                                h1_ok = False
                                break
    except Exception:
        h1_ok = False
        
    # neg_Q: The number of distinct subgroups of G that are conjugate to H is NOT equal to the index of N_G(H) in G
    try:
        G_elems = []
        for i, g in enumerate(get_elements(G)):
            if i >= 10000:
                break
            G_elems.append(g)
            
        H_elems = []
        for i, h in enumerate(get_elements(H)):
            if i >= 10000:
                break
            H_elems.append(h)
            
        if G_elems and isinstance(G_elems[0], Permutation):
            degree = max(
                max((p.size for p in G_elems), default=0),
                max((p.size for p in H_elems), default=0)
            )
            def pad(p, d):
                if p.size >= d:
                    return p
                return Permutation(p.array_form + list(range(p.size, d)))
            
            G_elems = [pad(g, degree) for g in G_elems]
            H_elems = [pad(h, degree) for h in H_elems]
            
        H_set = frozenset(H_elems)
        conjugates = set()
        norm_order = 0
        
        for g in G_elems:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g.inv()
            
            conj_set = frozenset(g * h * g_inv for h in H_set)
            conjugates.add(conj_set)
            if conj_set == H_set:
                norm_order += 1
                
        num_conjugates = len(conjugates)
        order_G = len(G_elems)
        
        neg_q_ok = (num_conjugates * norm_order != order_G)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "not Q: The number of distinct subgroups of G conjugate to H is not equal to the index of N_G(H) in G"
]

N_HYP = 1
NEG_Q_INDEX = 1