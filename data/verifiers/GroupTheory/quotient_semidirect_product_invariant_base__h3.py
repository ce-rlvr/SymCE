import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = PermutationGroup(Permutation(0, 1) * Permutation(2, 3), Permutation(0, 2) * Permutation(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    return list(G)

def get_phi(phi, h, n):
    if callable(phi):
        try:
            return phi(h, n)
        except Exception:
            return phi(h)(n)
    else:
        return phi[h][n]

def conditions(witness):
    """
    witness is expected to be a tuple: (N, H, phi, M)
    where:
      - N and H are groups (e.g., PermutationGroup)
      - phi is a homomorphism from H to Aut(N), provided as a dict of dicts or a callable
      - M is a normal subgroup of N
    """
    try:
        N, H, phi, M = witness
    except Exception:
        return [False, False, False]
        
    try:
        N_elems = get_elements(N)
        H_elems = get_elements(H)
    except Exception:
        return [False, False, False]

    # H_1: G = N rtimes_phi H is a valid semidirect product
    h1_ok = False
    try:
        valid_phi = True
        for h in H_elems:
            mapped = set()
            for n in N_elems:
                pn = get_phi(phi, h, n)
                if pn not in N_elems:
                    valid_phi = False
                    break
                mapped.add(pn)
            if not valid_phi or len(mapped) != len(N_elems):
                valid_phi = False
                break
            
            for n1 in N_elems:
                for n2 in N_elems:
                    if get_phi(phi, h, n1 * n2) != get_phi(phi, h, n1) * get_phi(phi, h, n2):
                        valid_phi = False
                        break
                if not valid_phi: break
            if not valid_phi: break
            
        if valid_phi:
            is_left_action = True
            is_right_action = True
            for h1 in H_elems:
                for h2 in H_elems:
                    for n in N_elems:
                        if get_phi(phi, h1 * h2, n) != get_phi(phi, h1, get_phi(phi, h2, n)):
                            is_left_action = False
                        if get_phi(phi, h1 * h2, n) != get_phi(phi, h2, get_phi(phi, h1, n)):
                            is_right_action = False
            if not (is_left_action or is_right_action):
                valid_phi = False
        h1_ok = valid_phi
    except Exception:
        h1_ok = False

    # H_2: M is a normal subgroup of N
    h2_ok = False
    try:
        M_elems = get_elements(M)
        if not M_elems:
            is_normal = False
        else:
            is_subgroup = True
            for m in M_elems:
                if m not in N_elems:
                    is_subgroup = False
                    break
            if is_subgroup:
                for m1 in M_elems:
                    for m2 in M_elems:
                        if m1 * m2 not in M_elems:
                            is_subgroup = False
                            break
                    if not is_subgroup: break
            if is_subgroup:
                for m in M_elems:
                    if m**-1 not in M_elems:
                        is_subgroup = False
                        break
            
            is_normal = is_subgroup
            if is_normal:
                for n in N_elems:
                    for m in M_elems:
                        if n * m * n**-1 not in M_elems:
                            is_normal = False
                            break
                    if not is_normal: break
            h2_ok = is_normal
    except Exception:
        h2_ok = False

    # neg_Q: M x {1_H} is NOT a normal subgroup of G
    neg_q_ok = False
    try:
        M_elems = get_elements(M)
        
        is_normal_in_G = True
        for h in H_elems:
            for m in M_elems:
                if get_phi(phi, h, m) not in M_elems:
                    is_normal_in_G = False
                    break
            if not is_normal_in_G:
                break
                
        neg_q_ok = not is_normal_in_G
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G = N rtimes_phi H is a valid semidirect product",
    "H_2: M is a normal subgroup of N",
    "¬Q: M x {1_H} is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2