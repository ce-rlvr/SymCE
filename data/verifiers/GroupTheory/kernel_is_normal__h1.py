import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "¬Q: The kernel of phi is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
            phi = witness
            G = phi.domain
            H = phi.codomain
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, H, phi = witness
        else:
            return [False, False]
            
        def apply_phi(phi_obj, x):
            if isinstance(phi_obj, dict):
                return phi_obj[x]
            elif isinstance(phi_obj, list):
                for k, v in phi_obj:
                    if k == x: 
                        return v
                raise ValueError("Mapping not found")
            return phi_obj(x)

        h1 = True
        if not hasattr(G, 'elements') or not hasattr(H, 'elements') or not hasattr(G, 'identity') or not hasattr(H, 'identity'):
            h1 = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            for x in G_elements:
                try:
                    px = apply_phi(phi, x)
                    if px not in H_elements:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
            
            if h1:
                for x in G_elements:
                    for y in G_elements:
                        try:
                            if apply_phi(phi, x * y) != apply_phi(phi, x) * apply_phi(phi, y):
                                h1 = False
                                break
                        except Exception:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    try:
        if not hasattr(G, 'elements') or not hasattr(H, 'identity') or not hasattr(G, 'identity'):
            return [h1, False]
            
        G_elements = list(G.elements)
        
        id_H_attr = getattr(H, 'identity', None)
        id_H = id_H_attr() if callable(id_H_attr) else id_H_attr
        
        id_G_attr = getattr(G, 'identity', None)
        id_G = id_G_attr() if callable(id_G_attr) else id_G_attr
        
        kernel = []
        for x in G_elements:
            try:
                if apply_phi(phi, x) == id_H:
                    kernel.append(x)
            except Exception:
                pass
                
        is_subgroup = True
        if id_G not in kernel:
            is_subgroup = False
        else:
            for x in kernel:
                for y in kernel:
                    if x * y not in kernel:
                        is_subgroup = False
                        break
                try:
                    if x**-1 not in kernel:
                        is_subgroup = False
                        break
                except Exception:
                    is_subgroup = False
                    break
                if not is_subgroup:
                    break
                    
        is_normal = True
        if is_subgroup:
            for k in kernel:
                for g in G_elements:
                    try:
                        if g * k * (g**-1) not in kernel:
                            is_normal = False
                            break
                    except Exception:
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
            
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]