import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]

    def apply_phi(g):
        if isinstance(phi, dict):
            return phi[g]
        else:
            return phi(g)

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            try:
                H_elements = list(H.elements)
            except AttributeError:
                try:
                    H_elements = list(H.generate())
                except Exception:
                    H_elements = list(H)
            
            try:
                G_elements = list(G.elements)
            except AttributeError:
                try:
                    G_elements = list(G.generate())
                except Exception:
                    G_elements = list(G)
                    
            h1 = True
            for h in H_elements:
                if h not in G_elements:
                    h1 = False
                    break
            if h1:
                for h1_el in H_elements:
                    for h2_el in H_elements:
                        if h1_el * h2_el not in H_elements:
                            h1 = False
                            break
                    if not h1:
                        break
            if h1:
                if len(H_elements) == 0:
                    h1 = False
    except Exception:
        h1 = False

    # H_2: phi is an automorphism of G
    try:
        try:
            G_elements = list(G.elements)
        except AttributeError:
            try:
                G_elements = list(G.generate())
            except Exception:
                G_elements = list(G)
                
        phi_values = []
        for g in G_elements:
            phi_values.append(apply_phi(g))
            
        h2 = True
        if len(phi_values) != len(G_elements):
            h2 = False
        else:
            for g in G_elements:
                if g not in phi_values:
                    h2 = False
                    break
            for v in phi_values:
                if v not in G_elements:
                    h2 = False
                    break
                    
        if h2:
            for g1 in G_elements:
                for g2 in G_elements:
                    if apply_phi(g1 * g2) != apply_phi(g1) * apply_phi(g2):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: N_G(H) denotes the normalizer of H in G
    h3 = True

    # neg_Q: N_G(phi(H)) != phi(N_G(H))
    try:
        try:
            G_elements = list(G.elements)
        except AttributeError:
            try:
                G_elements = list(G.generate())
            except Exception:
                G_elements = list(G)
                
        try:
            H_elements = list(H.elements)
        except AttributeError:
            try:
                H_elements = list(H.generate())
            except Exception:
                H_elements = list(H)
                
        H_list = list(H_elements)
        
        def is_in_normalizer(g, sub_list):
            try:
                g_inv = g**-1
            except Exception:
                return False
            for h in sub_list:
                if (g * h * g_inv) not in sub_list:
                    return False
            return True
            
        N_G_H = [g for g in G_elements if is_in_normalizer(g, H_list)]
        
        phi_H_list = [apply_phi(h) for h in H_list]
        
        N_G_phi_H = [g for g in G_elements if is_in_normalizer(g, phi_H_list)]
        
        phi_N_G_H = [apply_phi(g) for g in N_G_H]
        
        def lists_equal_as_sets(l1, l2):
            for x in l1:
                if x not in l2:
                    return False
            for x in l2:
                if x not in l1:
                    return False
            return True
            
        neg_q = not lists_equal_as_sets(N_G_phi_H, phi_N_G_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: phi is an automorphism of G",
    "H_3: N_G(H) denotes the normalizer of H in G",
    "¬Q: N_G(phi(H)) != phi(N_G(H))"
]

N_HYP = 3
NEG_Q_INDEX = 3