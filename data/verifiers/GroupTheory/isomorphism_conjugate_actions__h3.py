import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
Z8 = CyclicGroup(8)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a homomorphism from H to Aut(N)",
    "H_3: psi is a homomorphism from H to Aut(N)",
    "¬Q: The semidirect products N rtimes_phi H and N rtimes_psi H are not isomorphic"
]
N_HYP = 3
NEG_Q_INDEX = 3

def apply_map(mapping, h, n):
    if callable(mapping):
        return mapping(h, n)
    elif isinstance(mapping, dict):
        if (h, n) in mapping:
            return mapping[(h, n)]
        elif h in mapping:
            val = mapping[h]
            if callable(val):
                return val(n)
            elif isinstance(val, dict):
                return val[n]
    raise ValueError("Mapping must be callable or dict")

def build_perm_group(elems, mult):
    n = len(elems)
    elem_to_idx = {e: i for i, e in enumerate(elems)}
    perms = []
    for g in elems:
        p_list = [0] * n
        for x in elems:
            gx = mult(g, x)
            p_list[elem_to_idx[x]] = elem_to_idx[gx]
        perms.append(Permutation(p_list))
    return PermutationGroup(*perms)

def conditions(witness):
    try:
        N, H, phi, psi = witness
    except Exception:
        return [False, False, False, False]

    # H_1: N and H are groups
    try:
        N_elems = list(N.generate()) if hasattr(N, 'generate') else list(N.elements)
        H_elems = list(H.generate()) if hasattr(H, 'generate') else list(H.elements)
        N_id = N.identity
        H_id = H.identity
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: phi is a homomorphism from H to Aut(N)
    try:
        h2_ok = True
        if h1_ok:
            # Check closure
            for h in H_elems:
                for n in N_elems:
                    if apply_map(phi, h, n) not in N_elems:
                        h2_ok = False
                        break
                if not h2_ok: break
            
            # Check phi(h) is a homomorphism N -> N
            if h2_ok:
                for h in H_elems:
                    for n1 in N_elems:
                        for n2 in N_elems:
                            if apply_map(phi, h, n1 * n2) != apply_map(phi, h, n1) * apply_map(phi, h, n2):
                                h2_ok = False
                                break
                        if not h2_ok: break
                    if not h2_ok: break
            
            # Check phi(h) is a bijection (automorphism)
            if h2_ok:
                for h in H_elems:
                    img = set(apply_map(phi, h, n) for n in N_elems)
                    if len(img) != len(N_elems):
                        h2_ok = False
                        break
            
            # Check phi is a homomorphism H -> Aut(N)
            if h2_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        for n in N_elems:
                            if apply_map(phi, h1 * h2, n) != apply_map(phi, h1, apply_map(phi, h2, n)):
                                h2_ok = False
                                break
                        if not h2_ok: break
                    if not h2_ok: break
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # H_3: psi is a homomorphism from H to Aut(N)
    try:
        h3_ok = True
        if h1_ok:
            # Check closure
            for h in H_elems:
                for n in N_elems:
                    if apply_map(psi, h, n) not in N_elems:
                        h3_ok = False
                        break
                if not h3_ok: break
            
            # Check psi(h) is a homomorphism N -> N
            if h3_ok:
                for h in H_elems:
                    for n1 in N_elems:
                        for n2 in N_elems:
                            if apply_map(psi, h, n1 * n2) != apply_map(psi, h, n1) * apply_map(psi, h, n2):
                                h3_ok = False
                                break
                        if not h3_ok: break
                    if not h3_ok: break
            
            # Check psi(h) is a bijection (automorphism)
            if h3_ok:
                for h in H_elems:
                    img = set(apply_map(psi, h, n) for n in N_elems)
                    if len(img) != len(N_elems):
                        h3_ok = False
                        break
            
            # Check psi is a homomorphism H -> Aut(N)
            if h3_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        for n in N_elems:
                            if apply_map(psi, h1 * h2, n) != apply_map(psi, h1, apply_map(psi, h2, n)):
                                h3_ok = False
                                break
                        if not h3_ok: break
                    if not h3_ok: break
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: The semidirect products N rtimes_phi H and N rtimes_psi H are NOT isomorphic
    try:
        neg_q_ok = False
        if h1_ok and h2_ok and h3_ok:
            G1_elems = [(n, h) for n in N_elems for h in H_elems]
            def G1_mult(e1, e2):
                n1, h1 = e1
                n2, h2 = e2
                return (n1 * apply_map(phi, h1, n2), h1 * h2)
                
            G2_elems = [(n, h) for n in N_elems for h in H_elems]
            def G2_mult(e1, e2):
                n1, h1 = e1
                n2, h2 = e2
                return (n1 * apply_map(psi, h1, n2), h1 * h2)
                
            def get_orders(elems, mult, identity):
                orders = []
                for g in elems:
                    curr = g
                    order = 1
                    while curr != identity:
                        curr = mult(curr, g)
                        order += 1
                        if order > len(elems):
                            break
                    orders.append(order)
                return sorted(orders)
                
            id1 = (N_id, H_id)
            id2 = (N_id, H_id)
            
            orders1 = get_orders(G1_elems, G1_mult, id1)
            orders2 = get_orders(G2_elems, G2_mult, id2)
            
            if orders1 != orders2:
                neg_q_ok = True
            else:
                def get_center_size(elems, mult):
                    size = 0
                    for g in elems:
                        is_central = True
                        for x in elems:
                            if mult(g, x) != mult(x, g):
                                is_central = False
                                break
                        if is_central:
                            size += 1
                    return size
                    
                if get_center_size(G1_elems, G1_mult) != get_center_size(G2_elems, G2_mult):
                    neg_q_ok = True
                else:
                    G1_perm = build_perm_group(G1_elems, G1_mult)
                    G2_perm = build_perm_group(G2_elems, G2_mult)
                    neg_q_ok = not G1_perm.is_isomorphic(G2_perm)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]