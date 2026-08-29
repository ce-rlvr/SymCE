import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]

    # H1: H is a group (and N is a group)
    try:
        N_elems = list(N.elements) if hasattr(N, 'elements') else list(N)
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
        
        def find_identity(elems):
            for e in elems:
                if all(e * x == x for x in elems) and all(x * e == x for x in elems):
                    return e
            return None
            
        id_N = N.identity if hasattr(N, 'identity') else find_identity(N_elems)
        id_H = H.identity if hasattr(H, 'identity') else find_identity(H_elems)
        
        h1_ok = (id_N is not None) and (id_H is not None) and len(N_elems) > 0 and len(H_elems) > 0
        
        if h1_ok:
            for a in H_elems:
                for b in H_elems:
                    if a * b not in H_elems:
                        h1_ok = False
                        break
                if not h1_ok: break
            for a in N_elems:
                for b in N_elems:
                    if a * b not in N_elems:
                        h1_ok = False
                        break
                if not h1_ok: break

        if h1_ok:
            for a in H_elems:
                has_inv = False
                for b in H_elems:
                    if a * b == id_H and b * a == id_H:
                        has_inv = True
                        break
                if not has_inv:
                    h1_ok = False
                    break
            for a in N_elems:
                has_inv = False
                for b in N_elems:
                    if a * b == id_N and b * a == id_N:
                        has_inv = True
                        break
                if not has_inv:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    def get_phi(h, n):
        mapping = phi(h) if callable(phi) else phi[h]
        return mapping(n) if callable(mapping) else mapping[n]

    # H2: phi is an injective group homomorphism from H to Aut(N)
    try:
        h2_ok = True
        for h in H_elems:
            mapped_elements = []
            for n in N_elems:
                mapped_n = get_phi(h, n)
                if mapped_n not in mapped_elements:
                    mapped_elements.append(mapped_n)
            if len(mapped_elements) != len(N_elems):
                h2_ok = False
                break
            for n1 in N_elems:
                for n2 in N_elems:
                    if get_phi(h, n1 * n2) != get_phi(h, n1) * get_phi(h, n2):
                        h2_ok = False
                        break
                if not h2_ok: break
            if not h2_ok: break
            
        if h2_ok:
            for h1 in H_elems:
                for h2 in H_elems:
                    h12 = h1 * h2
                    for n in N_elems:
                        if get_phi(h12, n) != get_phi(h1, get_phi(h2, n)):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
                
        if h2_ok:
            for h1 in H_elems:
                for h2 in H_elems:
                    if h1 != h2:
                        same = True
                        for n in N_elems:
                            if get_phi(h1, n) != get_phi(h2, n):
                                same = False
                                break
                        if same:
                            h2_ok = False
                            break
                if not h2_ok: break
    except Exception:
        h2_ok = False

    # neg_Q: The center of N rtimes H is NOT equal to the proposed subgroup
    try:
        G_elems = [(n, h) for n in N_elems for h in H_elems]
        
        def mul(x, y):
            n1, h1 = x
            n2, h2 = y
            return (n1 * get_phi(h1, n2), h1 * h2)
            
        center = []
        for g in G_elems:
            is_central = True
            for x in G_elems:
                if mul(g, x) != mul(x, g):
                    is_central = False
                    break
            if is_central:
                center.append(g)
                
        proposed_subgroup = []
        for n in N_elems:
            fixed_by_all = True
            for h in H_elems:
                if get_phi(h, n) != n:
                    fixed_by_all = False
                    break
            if fixed_by_all:
                proposed_subgroup.append((n, id_H))
                
        def is_equal_sets(list1, list2):
            for item in list1:
                if item not in list2: return False
            for item in list2:
                if item not in list1: return False
            return True
            
        neg_q = not is_equal_sets(center, proposed_subgroup)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: phi: H -> Aut(N) is an injective group homomorphism",
    "¬Q: The center of N rtimes H is NOT equal to the subgroup of elements (n, 1_H) fixed by all phi_h"
]

N_HYP = 2
NEG_Q_INDEX = 2