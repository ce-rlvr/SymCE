import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        H_explicit = None
        if isinstance(witness, dict):
            G = witness.get('G')
            phi_map = witness.get('phi_map')
            if 'H' in witness:
                H_explicit = witness['H']
                H_order = H_explicit.order()
                H_op = lambda x, y: x * y
            else:
                H_order = witness.get('H_order')
                H_op = witness.get('H_op')
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                G, H_order, phi_map, H_op = witness
            elif len(witness) == 3:
                G, H_explicit, phi_map = witness
                H_order = H_explicit.order()
                H_op = lambda x, y: x * y
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if G is None or phi_map is None or H_order is None or H_op is None:
            return [False, False, False]
            
        if hasattr(G, 'elements') and callable(phi_map):
            try:
                phi_map = {g: phi_map(g) for g in G.elements}
            except Exception:
                pass
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = False
        if hasattr(G, 'is_group') and G.is_group:
            if hasattr(G, 'order'):
                ord_G = float(G.order())
                if ord_G < float('inf') and ord_G > 0:
                    h1 = True
        elif hasattr(G, 'elements') and hasattr(G, 'order'):
            ord_G = float(G.order())
            if ord_G < float('inf') and ord_G > 0:
                h1 = True
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        h2 = False
        if h1:
            is_inf = False
            try:
                if H_order in [float('inf'), math.inf, sympy.oo] or str(H_order).lower() in ['oo', 'inf', 'infinity']:
                    is_inf = True
            except Exception:
                pass
            
            is_valid_order = is_inf
            if not is_valid_order:
                try:
                    if float(H_order) >= 1:
                        is_valid_order = True
                except Exception:
                    pass
            
            if is_valid_order:
                elements = list(G.elements)
                if isinstance(phi_map, dict) and all(g in phi_map for g in elements):
                    img_in_H = True
                    if H_explicit is not None:
                        try:
                            H_elements = list(H_explicit.elements)
                            if not all(phi_map[g] in H_elements for g in elements):
                                img_in_H = False
                        except Exception:
                            img_in_H = False
                            
                    if img_in_H:
                        is_homo = True
                        for x in elements:
                            for y in elements:
                                xy = x * y
                                if phi_map[xy] != H_op(phi_map[x], phi_map[y]):
                                    is_homo = False
                                    break
                            if not is_homo:
                                break
                        
                        if is_homo:
                            id_G = G.identity
                            id_H = phi_map[id_G]
                            ker_size = sum(1 for g in G.elements if phi_map[g] == id_H)
                            index = float(G.order()) / ker_size
                            
                            if not is_inf:
                                if abs(index - round(index)) > 1e-9:
                                    h2 = False
                                else:
                                    idx_int = int(round(index))
                                    if idx_int != 0 and int(H_order) % idx_int == 0:
                                        h2 = True
                                    else:
                                        h2 = False
                            else:
                                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The index of ker(phi) in G does not divide the order of H
    try:
        neg_q = False
        if h1 and h2:
            id_G = G.identity
            id_H = phi_map[id_G]
            
            ker_size = sum(1 for g in G.elements if phi_map[g] == id_H)
            index = float(G.order()) / ker_size
            
            is_inf = False
            try:
                if H_order in [float('inf'), math.inf, sympy.oo] or str(H_order).lower() in ['oo', 'inf', 'infinity']:
                    is_inf = True
            except Exception:
                pass
                
            if is_inf:
                divides = False
            else:
                if abs(index - round(index)) > 1e-9:
                    divides = False
                else:
                    idx_int = int(round(index))
                    if idx_int == 0:
                        divides = False
                    else:
                        try:
                            divides = (int(H_order) % idx_int == 0)
                        except Exception:
                            divides = False
            neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The index of ker(phi) in G does not divide the order of H"
]

N_HYP = 2
NEG_Q_INDEX = 2