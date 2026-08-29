import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    G = None
    H = None
    phi_dict = None
    elements_G = []
    elements_H = []
    
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, phi = witness
        else:
            phi = witness
            G = phi.domain
            H = phi.codomain
            
        if hasattr(G, 'elements'):
            elements_G = list(G.elements)
        elif hasattr(G, 'generate'):
            elements_G = list(G.generate())
            
        if hasattr(H, 'elements'):
            elements_H = list(H.elements)
        elif hasattr(H, 'generate'):
            elements_H = list(H.generate())
            
        if callable(phi):
            phi_dict = {g: phi(g) for g in elements_G}
        elif isinstance(phi, dict):
            phi_dict = phi
        elif hasattr(phi, 'domain') and hasattr(phi, 'codomain'):
            phi_dict = {g: phi(g) for g in elements_G}
    except Exception:
        pass

    # H_1: phi is a group homomorphism from G to H
    h1_ok = False
    try:
        if G is not None and H is not None and phi_dict is not None:
            if all(g in phi_dict for g in elements_G) and all(phi_dict[g] in elements_H for g in elements_G):
                is_hom = True
                for x in elements_G:
                    for y in elements_G:
                        if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                h1_ok = is_hom
    except Exception:
        h1_ok = False

    # ¬Q: ker(phi) is NOT a normal subgroup of G
    neg_q_ok = False
    try:
        if G is not None and H is not None and phi_dict is not None:
            if hasattr(H, 'identity'):
                id_H = H.identity
            else:
                id_H = next((e for e in elements_H if e * e == e), None)
                
            if hasattr(G, 'identity'):
                id_G = G.identity
            else:
                id_G = next((e for e in elements_G if e * e == e), None)

            if id_H is not None and id_G is not None:
                ker = set()
                for g in elements_G:
                    if g in phi_dict and phi_dict[g] == id_H:
                        ker.add(g)
                
                is_subgroup = True
                if id_G not in ker:
                    is_subgroup = False
                else:
                    for x in ker:
                        inv_x = None
                        if hasattr(x, '__pow__'):
                            try:
                                inv_x = x**-1
                            except Exception:
                                pass
                        if inv_x is None:
                            inv_x = next((y for y in elements_G if x * y == id_G), None)
                            
                        if inv_x not in ker:
                            is_subgroup = False
                            break
                            
                        for y in ker:
                            if x * y not in ker:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                
                if not is_subgroup:
                    neg_q_ok = True
                else:
                    is_normal = True
                    for g in elements_G:
                        inv_g = None
                        if hasattr(g, '__pow__'):
                            try:
                                inv_g = g**-1
                            except Exception:
                                pass
                        if inv_g is None:
                            inv_g = next((y for y in elements_G if g * y == id_G), None)
                            
                        for k in ker:
                            if g * k * inv_g not in ker:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    neg_q_ok = not is_normal
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "¬Q: ker(phi) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1