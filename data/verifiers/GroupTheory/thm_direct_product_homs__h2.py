import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G1, G2, H1, H2, phi1, phi2 = witness
    except Exception:
        return [False, False]
        
    def eval_map(phi, g):
        if isinstance(phi, dict):
            return phi.get(g, None)
        else:
            try:
                return phi(g)
            except Exception:
                return None

    def get_identity(G):
        for g in G.elements:
            is_id = True
            for x in G.elements:
                if g * x != x:
                    is_id = False
                    break
            if is_id:
                return g
        return None

    # H_1: phi_1 is a group homomorphism from G_1 to H_1
    try:
        h1_ok = True
        for g in G1.elements:
            val = eval_map(phi1, g)
            if val is None or val not in H1.elements:
                h1_ok = False
                break
        if h1_ok:
            for g1 in G1.elements:
                for g2 in G1.elements:
                    if eval_map(phi1, g1 * g2) != eval_map(phi1, g1) * eval_map(phi1, g2):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # neg_Q: phi is NOT a group homomorphism OR its kernel is NOT ker(phi_1) x ker(phi_2)
    try:
        neg_q = False
        
        # Check if phi is a well-defined map
        is_map1 = True
        for g in G1.elements:
            val = eval_map(phi1, g)
            if val is None or val not in H1.elements:
                is_map1 = False
                break
                
        is_map2 = True
        for g in G2.elements:
            val = eval_map(phi2, g)
            if val is None or val not in H2.elements:
                is_map2 = False
                break
                
        if not is_map1 or not is_map2:
            neg_q = True
        else:
            # Check if phi is a homomorphism
            is_hom = True
            for x1 in G1.elements:
                for x2 in G1.elements:
                    if eval_map(phi1, x1 * x2) != eval_map(phi1, x1) * eval_map(phi1, x2):
                        is_hom = False
                        break
                if not is_hom: break
                
            if is_hom:
                for y1 in G2.elements:
                    for y2 in G2.elements:
                        if eval_map(phi2, y1 * y2) != eval_map(phi2, y1) * eval_map(phi2, y2):
                            is_hom = False
                            break
                    if not is_hom: break
                
            if not is_hom:
                neg_q = True
            else:
                # Check kernel
                id_H1 = get_identity(H1)
                id_H2 = get_identity(H2)
                
                ker_phi = set()
                for x in G1.elements:
                    for y in G2.elements:
                        if eval_map(phi1, x) == id_H1 and eval_map(phi2, y) == id_H2:
                            ker_phi.add((x, y))
                            
                ker_phi1 = set(x for x in G1.elements if eval_map(phi1, x) == id_H1)
                ker_phi2 = set(y for y in G2.elements if eval_map(phi2, y) == id_H2)
                
                ker_prod = set((x, y) for x in ker_phi1 for y in ker_phi2)
                
                if ker_phi != ker_prod:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi_1 is a group homomorphism from G_1 to H_1",
    "¬Q: phi is not a group homomorphism or its kernel is not ker(phi_1) x ker(phi_2)"
]

N_HYP = 1
NEG_Q_INDEX = 1