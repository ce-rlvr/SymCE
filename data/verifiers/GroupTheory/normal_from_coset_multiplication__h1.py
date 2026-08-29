import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
    "H_1: H is a subgroup of G",
    "H_2: For all a, b in G, (aH)(bH) = (ab)H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    return list(group)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False]
            
        if G is None or H is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1_ok = bool(H.is_subgroup(G))
        else:
            H_elems = get_elements(H)
            G_elems = get_elements(G)
            try:
                H_set = set(H_elems)
                G_set = set(G_elems)
                if not H_set.issubset(G_set):
                    h1_ok = False
                else:
                    h1_ok = True
                    for h1 in H_elems:
                        for h2 in H_elems:
                            if h1 * h2 not in H_set:
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
            except TypeError:
                # Fallback for unhashable elements (like mutable matrices)
                if not all(x in G_elems for x in H_elems):
                    h1_ok = False
                else:
                    h1_ok = True
                    for h1 in H_elems:
                        for h2 in H_elems:
                            if h1 * h2 not in H_elems:
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
    except Exception:
        h1_ok = False

    # H_2: For all a, b in G, (aH)(bH) = (ab)H
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        h2_ok = True
        for a in G_elems:
            for b in G_elems:
                try:
                    aHbH = {a * h1 * b * h2 for h1 in H_elems for h2 in H_elems}
                    abH = {a * b * h for h in H_elems}
                    if aHbH != abH:
                        h2_ok = False
                        break
                except TypeError:
                    # Fallback for unhashable elements
                    aHbH_list = []
                    for h1 in H_elems:
                        for h2 in H_elems:
                            val = a * h1 * b * h2
                            if val not in aHbH_list:
                                aHbH_list.append(val)
                    abH_list = []
                    ab = a * b
                    for h in H_elems:
                        val = ab * h
                        if val not in abH_list:
                            abH_list.append(val)
                    if len(aHbH_list) != len(abH_list) or any(x not in abH_list for x in aHbH_list):
                        h2_ok = False
                        break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # ¬Q: H is not a normal subgroup of G
    try:
        if hasattr(H, 'is_normal'):
            neg_q_ok = not bool(H.is_normal(G))
        else:
            G_elems = get_elements(G)
            H_elems = get_elements(H)
            try:
                H_set = set(H_elems)
            except TypeError:
                H_set = H_elems
                
            is_norm = True
            for g in G_elems:
                try:
                    ginv = ~g
                except Exception:
                    ginv = g**-1
                for h in H_elems:
                    if g * h * ginv not in H_set:
                        is_norm = False
                        break
                if not is_norm:
                    break
            neg_q_ok = not is_norm
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]