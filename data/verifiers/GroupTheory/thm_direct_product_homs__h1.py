import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def evaluate_map(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    else:
        return phi(x)

def conditions(witness):
    try:
        G1 = witness["G1"]
        G2 = witness["G2"]
        H1 = witness["H1"]
        H2 = witness["H2"]
        phi1 = witness["phi1"]
        phi2 = witness["phi2"]
        
        for g in [G1, G2, H1, H2]:
            _ = g.elements
            _ = g.identity
    except Exception:
        return [False, False]
        
    # H1: phi2 is a homomorphism from G2 to H2
    h1_ok = False
    try:
        H2_elems = set(H2.elements)
        is_hom = True
        for x in G2.elements:
            px = evaluate_map(phi2, x)
            if px not in H2_elems:
                is_hom = False
                break
        if is_hom:
            for x in G2.elements:
                for y in G2.elements:
                    px = evaluate_map(phi2, x)
                    py = evaluate_map(phi2, y)
                    pxy = evaluate_map(phi2, x * y)
                    if pxy != px * py:
                        is_hom = False
                        break
                if not is_hom:
                    break
        h1_ok = is_hom
    except Exception:
        h1_ok = False

    # neg_Q: phi is NOT a homomorphism from G1xG2 to H1xH2 OR ker(phi) != ker(phi1) x ker(phi2)
    neg_q_ok = False
    try:
        conclusion_holds = True
        H1_elems = set(H1.elements)
        H2_elems = set(H2.elements)
        
        # Check if phi maps G1xG2 into H1xH2
        for x in G1.elements:
            px = evaluate_map(phi1, x)
            if px not in H1_elems:
                conclusion_holds = False
                break
        if conclusion_holds:
            for y in G2.elements:
                py = evaluate_map(phi2, y)
                if py not in H2_elems:
                    conclusion_holds = False
                    break
                    
        # Check if phi is a homomorphism
        if conclusion_holds:
            for x1 in G1.elements:
                for y1 in G2.elements:
                    for x2 in G1.elements:
                        for y2 in G2.elements:
                            px1 = evaluate_map(phi1, x1)
                            py1 = evaluate_map(phi2, y1)
                            px2 = evaluate_map(phi1, x2)
                            py2 = evaluate_map(phi2, y2)
                            
                            px12 = evaluate_map(phi1, x1 * x2)
                            py12 = evaluate_map(phi2, y1 * y2)
                            
                            if px12 != px1 * px2 or py12 != py1 * py2:
                                conclusion_holds = False
                                break
                        if not conclusion_holds:
                            break
                    if not conclusion_holds:
                        break
                if not conclusion_holds:
                    break
                    
        # Check kernel
        if conclusion_holds:
            ker_phi1 = {x for x in G1.elements if evaluate_map(phi1, x) == H1.identity}
            ker_phi2 = {y for y in G2.elements if evaluate_map(phi2, y) == H2.identity}
            
            ker_phi = set()
            for x in G1.elements:
                for y in G2.elements:
                    if evaluate_map(phi1, x) == H1.identity and evaluate_map(phi2, y) == H2.identity:
                        ker_phi.add((x, y))
                        
            expected_ker = {(x, y) for x in ker_phi1 for y in ker_phi2}
            if ker_phi != expected_ker:
                conclusion_holds = False
                
        neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi_2 is a group homomorphism from G_2 to H_2",
    "¬Q: phi is not a group homomorphism from G_1 x G_2 to H_1 x H_2 with kernel ker(phi_1) x ker(phi_2)"
]

N_HYP = 1
NEG_Q_INDEX = 1