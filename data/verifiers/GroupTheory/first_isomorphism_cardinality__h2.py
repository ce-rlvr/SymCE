import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    "H_1: G is a finite group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The order of G does not equal the order of ker(phi) multiplied by the order of im(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, phi = witness
    except Exception:
        return [False, False, False]
        
    def get_elements(group, max_elements=2000):
        elements = []
        try:
            if hasattr(group, 'generate'):
                iterable = group.generate()
            elif hasattr(group, 'elements'):
                iterable = group.elements
            else:
                iterable = group
            for i, e in enumerate(iterable):
                if i >= max_elements:
                    return None
                elements.append(e)
            return elements
        except Exception:
            return None
            
    def get_identity(group):
        try:
            if hasattr(group, 'identity'):
                return group.identity
            elements = get_elements(group)
            if elements is None:
                return None
            for e in elements:
                is_id = True
                for x in elements:
                    try:
                        if e * x != x or x * e != x:
                            is_id = False
                            break
                    except Exception:
                        is_id = False
                        break
                if is_id:
                    return e
            return None
        except Exception:
            return None

    # H1: G is a finite group
    h1 = False
    try:
        elements_G = get_elements(G)
        if elements_G is not None and len(elements_G) > 0:
            closed = True
            for x in elements_G:
                for y in elements_G:
                    try:
                        if x * y not in elements_G:
                            closed = False
                            break
                    except Exception:
                        closed = False
                        break
                if not closed:
                    break
            if closed:
                id_G = get_identity(G)
                if id_G is not None:
                    inverses_ok = True
                    for x in elements_G:
                        has_inv = False
                        for y in elements_G:
                            try:
                                if x * y == id_G and y * x == id_G:
                                    has_inv = True
                                    break
                            except Exception:
                                pass
                        if not has_inv:
                            inverses_ok = False
                            break
                    if inverses_ok:
                        h1 = True
    except Exception:
        h1 = False

    # H2: phi is a group homomorphism from G to H
    h2 = False
    try:
        elements_G = get_elements(G)
        if elements_G is not None:
            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            else:
                phi_func = phi
                
            is_hom = True
            for x in elements_G:
                for y in elements_G:
                    try:
                        if phi_func(x * y) != phi_func(x) * phi_func(y):
                            is_hom = False
                            break
                    except Exception:
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            elements_H = get_elements(H)
            if is_hom and elements_H is not None:
                for x in elements_G:
                    try:
                        if phi_func(x) not in elements_H:
                            is_hom = False
                            break
                    except Exception:
                        is_hom = False
                        break
            elif is_hom:
                for x in elements_G:
                    try:
                        if phi_func(x) not in H:
                            is_hom = False
                            break
                    except Exception:
                        pass
                        
            if is_hom:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: |G| != |ker(phi)| * |im(phi)|
    neg_q = False
    try:
        elements_G = get_elements(G)
        if elements_G is not None:
            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            else:
                phi_func = phi
                
            id_G = get_identity(G)
            id_H = get_identity(H)
            
            if id_H is None:
                id_H = phi_func(id_G)
                
            ker_phi = []
            for x in elements_G:
                try:
                    if phi_func(x) == id_H:
                        ker_phi.append(x)
                except Exception:
                    pass
            
            im_phi = []
            for x in elements_G:
                try:
                    val = phi_func(x)
                    if val not in im_phi:
                        im_phi.append(val)
                except Exception:
                    pass
                    
            order_G = len(elements_G)
            order_ker = len(ker_phi)
            order_im = len(im_phi)
            
            neg_q = (order_G != order_ker * order_im)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]