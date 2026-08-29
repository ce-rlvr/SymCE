import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The kernel of phi is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def apply_op(op, x, y):
    if callable(op):
        return op(x, y)
    try:
        return op[(x, y)]
    except (TypeError, KeyError):
        return op[x][y]

def apply_phi(phi, x):
    if callable(phi):
        return phi(x)
    return phi[x]

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            op = witness.get('op')
            phi = witness.get('phi')
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            G, H, op, phi = witness
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            op = getattr(witness, 'op', None)
            phi = getattr(witness, 'phi', None)
    except Exception:
        return [False, False, False]

    try:
        G = list(G)
    except Exception:
        return [False, False, False]

    # H_1: H is a group
    try:
        h1_ok = False
        if isinstance(H, PermutationGroup):
            h1_ok = True
        else:
            elements = list(H)
            if elements:
                identities = []
                for e in elements:
                    if all(e * x == x and x * e == x for x in elements):
                        identities.append(e)
                if identities:
                    e = identities[0]
                    is_group = True
                    for x in elements:
                        has_inv = False
                        for y in elements:
                            if x * y not in elements:
                                is_group = False
                                break
                            if x * y == e and y * x == e:
                                has_inv = True
                        if not has_inv or not is_group:
                            is_group = False
                            break
                    h1_ok = is_group
    except Exception:
        h1_ok = False

    # Helper for H_2 and neg_Q
    try:
        if isinstance(H, PermutationGroup):
            id_H = H.identity
            def h_contains(x): return x in H
            def h_mul(x, y): return x * y
        else:
            elements = list(H)
            id_H = None
            for e in elements:
                if all(e * x == x and x * e == x for x in elements):
                    id_H = e
                    break
            def h_contains(x): return x in elements
            def h_mul(x, y): return x * y
    except Exception:
        id_H = None
        def h_contains(x): return False
        def h_mul(x, y): return None

    # H_2: \phi is a group homomorphism from G to H
    try:
        h2_ok = False
        if id_H is not None:
            is_hom = True
            for x in G:
                px = apply_phi(phi, x)
                if not h_contains(px):
                    is_hom = False
                    break
            if is_hom:
                for x in G:
                    for y in G:
                        xy = apply_op(op, x, y)
                        if xy not in G:
                            is_hom = False
                            break
                        px = apply_phi(phi, x)
                        py = apply_phi(phi, y)
                        pxy = apply_phi(phi, xy)
                        if pxy != h_mul(px, py):
                            is_hom = False
                            break
                    if not is_hom:
                        break
            h2_ok = is_hom
    except Exception:
        h2_ok = False

    # neg_Q: The kernel of \phi is not a normal subgroup of G
    try:
        neg_q_ok = False
        if id_H is not None:
            K = []
            for x in G:
                px = apply_phi(phi, x)
                if px == id_H:
                    K.append(x)
            
            is_normal_subgroup = True
            if not K:
                is_normal_subgroup = False
            else:
                # 1. Check closure
                for x in K:
                    for y in K:
                        xy = apply_op(op, x, y)
                        if xy not in K:
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
                
                if is_normal_subgroup:
                    # 2. Find identity in K
                    identities = []
                    for e in K:
                        is_id = True
                        for x in K:
                            ex = apply_op(op, e, x)
                            xe = apply_op(op, x, e)
                            if ex != x or xe != x:
                                is_id = False
                                break
                        if is_id:
                            identities.append(e)
                    
                    if not identities:
                        is_normal_subgroup = False
                    else:
                        e_K = identities[0]
                        # 3. Check inverses in K
                        for x in K:
                            has_inv = False
                            for y in K:
                                xy = apply_op(op, x, y)
                                yx = apply_op(op, y, x)
                                if xy == e_K and yx == e_K:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_normal_subgroup = False
                                break
                        
                        if is_normal_subgroup:
                            # 4. Check normality in G
                            for g in G:
                                left_coset = []
                                right_coset = []
                                for k in K:
                                    gk = apply_op(op, g, k)
                                    kg = apply_op(op, k, g)
                                    left_coset.append(gk)
                                    right_coset.append(kg)
                                
                                for x in left_coset:
                                    if x not in right_coset:
                                        is_normal_subgroup = False
                                        break
                                for x in right_coset:
                                    if x not in left_coset:
                                        is_normal_subgroup = False
                                        break
                                if not is_normal_subgroup:
                                    break
            neg_q_ok = not is_normal_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]