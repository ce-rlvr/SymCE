import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.homomorphisms import GroupHomomorphism, homomorphism
from sympy import eye, zeros, oo
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: The order of G does not equal the order of ker(phi) multiplied by the order of im(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(group):
    from sympy import oo
    if hasattr(group, 'order'):
        if callable(group.order):
            try:
                return group.order()
            except Exception:
                pass
        else:
            return group.order
    if hasattr(group, 'is_finite') and not group.is_finite:
        return oo
    if hasattr(group, 'elements'):
        try:
            return len(list(group.elements))
        except Exception:
            pass
    try:
        return len(group)
    except Exception:
        return None

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, H, phi = witness
        elif len(witness) == 2:
            G, phi = witness
            H = getattr(phi, 'codomain', None)
        else:
            return [False, False, False]
    else:
        phi = witness
        G = getattr(phi, 'domain', None)
        H = getattr(phi, 'codomain', None)

    # H1: H is a finite group
    try:
        h1 = False
        if H is not None:
            ord_H = get_order(H)
            from sympy import oo
            if ord_H is not None and ord_H != oo:
                try:
                    if int(ord_H) >= 1:
                        h1 = True
                except Exception:
                    pass
    except Exception:
        h1 = False

    # H2: phi is a group homomorphism from G to H
    try:
        h2 = False
        from sympy.combinatorics.homomorphisms import GroupHomomorphism
        if isinstance(phi, GroupHomomorphism):
            if phi.domain == G and phi.codomain == H:
                h2 = True
        else:
            is_hom = False
            if hasattr(phi, 'is_homomorphism'):
                is_hom = phi.is_homomorphism() if callable(phi.is_homomorphism) else phi.is_homomorphism
            elif hasattr(phi, 'is_hom'):
                is_hom = phi.is_hom() if callable(phi.is_hom) else phi.is_hom
            
            if is_hom:
                d = getattr(phi, 'domain', None)
                c = getattr(phi, 'codomain', None)
                if d == G and c == H:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: The order of G does not equal the order of ker(phi) multiplied by the order of im(phi)
    try:
        q = False
        if G is not None and phi is not None:
            order_G = get_order(G)
            
            ker = None
            if hasattr(phi, 'kernel'):
                ker = phi.kernel() if callable(phi.kernel) else phi.kernel
            order_ker = get_order(ker) if ker is not None else None
            
            im = None
            if hasattr(phi, 'image'):
                im = phi.image() if callable(phi.image) else phi.image
            order_im = get_order(im) if im is not None else None
            
            from sympy import oo
            if order_G is not None and order_ker is not None and order_im is not None:
                if order_G == oo or order_ker == oo or order_im == oo:
                    q = False
                else:
                    try:
                        q = (int(order_G) == int(order_ker) * int(order_im))
                    except Exception:
                        q = False
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, neg_q]