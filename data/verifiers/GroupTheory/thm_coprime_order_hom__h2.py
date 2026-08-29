import sympy
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
    # Extract G, H, phi from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, H, phi = witness
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            phi = getattr(witness, 'phi', None)
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    h1 = False
    try:
        if hasattr(G, 'is_group') and G.is_group:
            if hasattr(G, 'order'):
                o = G.order
                if callable(o):
                    o = o()
                if o != sympy.oo and o > 0:
                    h1 = True
        elif G.__class__.__name__ in ['SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup', 'PermutationGroup']:
            h1 = True
        elif hasattr(G, 'elements'):
            h1 = True
        elif isinstance(G, (list, tuple, set)) and len(G) > 0:
            h1 = True
    except Exception:
        pass

    # H_2: The orders of G and H are coprime, meaning \gcd(|G|, |H|) = 1
    h2 = False
    try:
        def get_order(grp):
            if hasattr(grp, 'order'):
                o = grp.order
                if callable(o):
                    o = o()
                return int(o)
            if hasattr(grp, 'elements'):
                return len(list(grp.elements))
            if isinstance(grp, (list, tuple, set)):
                return len(grp)
            raise ValueError("Cannot determine order")
        
        oG = get_order(G)
        oH = get_order(H)
        if math.gcd(oG, oH) == 1:
            h2 = True
    except Exception:
        pass

    # H_3: \phi: G \to H is a group homomorphism
    h3 = False
    try:
        if phi.__class__.__name__ == 'Homomorphism':
            h3 = True
        elif hasattr(phi, 'is_homomorphism'):
            res = phi.is_homomorphism
            if callable(res):
                res = res()
            if res:
                h3 = True
        else:
            elements = None
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif isinstance(G, (list, tuple, set)):
                elements = list(G)
            
            if elements is not None:
                is_hom = True
                for a in elements:
                    for b in elements:
                        ab = a * b
                        if isinstance(phi, dict):
                            pa = phi.get(a)
                            pb = phi.get(b)
                            pab = phi.get(ab)
                        else:
                            pa = phi(a)
                            pb = phi(b)
                            pab = phi(ab)
                        if pab != pa * pb:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                h3 = is_hom
    except Exception:
        pass

    # neg_Q: \phi is NOT the trivial homomorphism
    neg_q = False
    try:
        if phi.__class__.__name__ == 'Homomorphism':
            neg_q = not phi.is_trivial()
        elif hasattr(phi, 'is_trivial'):
            res = phi.is_trivial
            if callable(res):
                res = res()
            neg_q = not res
        else:
            elements = None
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif isinstance(G, (list, tuple, set)):
                elements = list(G)
            
            if elements is not None:
                id_H = None
                if hasattr(H, 'identity'):
                    id_H = H.identity
                elif hasattr(H, 'elements'):
                    for e in H.elements:
                        if e * e == e:
                            id_H = e
                            break
                elif isinstance(H, (list, tuple, set)):
                    for e in H:
                        if e * e == e:
                            id_H = e
                            break
                
                if id_H is not None:
                    is_trivial = True
                    for a in elements:
                        if isinstance(phi, dict):
                            pa = phi.get(a)
                        else:
                            pa = phi(a)
                        if pa != id_H:
                            is_trivial = False
                            break
                    neg_q = not is_trivial
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The orders of G and H are coprime",
    "H_3: phi is a group homomorphism",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3