import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    def get_elements(obj):
        if hasattr(obj, 'elements'):
            return list(obj.elements)
        elif hasattr(obj, 'generate'):
            return list(obj.generate())
        else:
            return list(obj)
            
    def get_inv(g):
        try:
            return g**-1
        except Exception:
            return ~g

    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
    except Exception:
        return [False, False, False]
        
    # H1: H is a subgroup of G
    try:
        manual_check = True
        if hasattr(H, 'is_subgroup'):
            try:
                h1 = bool(H.is_subgroup(G))
                manual_check = False
            except Exception:
                pass
                
        if manual_check:
            G_set = set(G_elems)
            H_set = set(H_elems)
            if not H_set.issubset(G_set) or not H_set:
                h1 = False
            else:
                h1 = True
                for h_a in H_set:
                    try:
                        inv = get_inv(h_a)
                        if inv not in H_set:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
                    for h_b in H_set:
                        if h_a * h_b not in H_set:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H2: G acts on the set of left cosets G/H via g \cdot (xH) = (gx)H
    try:
        def left_coset(x):
            return frozenset(x * h for h in H_elems)
            
        cosets = {left_coset(x) for x in G_elems}
        
        h2 = True
        # Check well-definedness
        for x in G_elems:
            for y in G_elems:
                if left_coset(x) == left_coset(y):
                    for g in G_elems:
                        if left_coset(g * x) != left_coset(g * y):
                            h2 = False
                            break
                if not h2: break
            if not h2: break
            
        # Check compatibility
        if h2:
            for g1 in G_elems:
                for g2 in G_elems:
                    for x in G_elems:
                        if left_coset(g1 * (g2 * x)) != left_coset((g1 * g2) * x):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # Q: The kernel of the action is \bigcap_{g \in G} gHg^{-1}, which is the largest normal subgroup of G contained in H.
    try:
        # 1. Find the kernel of the action
        K = set()
        for g in G_elems:
            acts_trivially = True
            for x in G_elems:
                if left_coset(g * x) != left_coset(x):
                    acts_trivially = False
                    break
            if acts_trivially:
                K.add(g)
                
        # 2. Find the intersection \bigcap_{g \in G} gHg^{-1}
        intersection = set(G_elems)
        for g in G_elems:
            g_inv = get_inv(g)
            gHg_inv = set(g * h * g_inv for h in H_elems)
            intersection = intersection.intersection(gHg_inv)
            
        if K != intersection:
            q = False
        else:
            # 3. Check if intersection is the largest normal subgroup of G contained in H
            is_normal = True
            for g in G_elems:
                g_inv = get_inv(g)
                for n in intersection:
                    if g * n * g_inv not in intersection:
                        is_normal = False
                        break
                if not is_normal: break
                
            is_contained = intersection.issubset(set(H_elems))
            
            if not is_normal or not is_contained:
                q = False
            else:
                is_largest = True
                for h in H_elems:
                    all_conjugates_in_H = True
                    for g in G_elems:
                        g_inv = get_inv(g)
                        if g * h * g_inv not in H_elems:
                            all_conjugates_in_H = False
                            break
                    if all_conjugates_in_H:
                        if h not in K:
                            is_largest = False
                            break
                q = is_largest
    except Exception:
        q = False

    neg_q = not q
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: G acts on the set of left cosets G/H via g \\cdot (xH) = (gx)H",
    "¬Q: The kernel of the action is not \\bigcap_{g \\in G} gHg^{-1} or it is not the largest normal subgroup of G contained in H"
]

N_HYP = 2
NEG_Q_INDEX = 2