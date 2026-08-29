import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            G = witness.G
            x = witness.x
    except Exception:
        return [False, False]

    # H_1: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h1 = bool(G.contains(x))
        elif hasattr(G, '__contains__'):
            try:
                h1 = bool(x in G)
            except Exception:
                h1 = True
        elif hasattr(G, 'elements'):
            h1 = bool(x in G.elements)
        else:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The size of the conjugacy class of x in G does not divide the index of the center of G
    try:
        size_cl = None
        if hasattr(G, 'conjugacy_class_size'):
            size_cl = G.conjugacy_class_size(x)
        elif hasattr(G, 'centralizer'):
            C_x = G.centralizer(x)
            if hasattr(G, 'index'):
                size_cl = G.index(C_x)
            elif hasattr(G, 'order') and hasattr(C_x, 'order'):
                g_ord = G.order()
                c_ord = C_x.order()
                if g_ord != sympy.oo:
                    size_cl = g_ord / c_ord
                elif c_ord == sympy.oo:
                    pass
                else:
                    size_cl = sympy.oo
        
        if size_cl is None:
            if hasattr(G, 'order') and G.order() == sympy.oo:
                raise ValueError("Cannot compute conjugacy class size for infinite group without custom methods")
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            orbit = set()
            for g in elements:
                try:
                    conj = g * x * g**-1
                except Exception:
                    conj = g * x * ~g
                orbit.add(conj)
            size_cl = len(orbit)

        index_Z = None
        if hasattr(G, 'center_index'):
            index_Z = G.center_index()
        elif hasattr(G, 'center'):
            Z = G.center()
            if hasattr(G, 'index'):
                index_Z = G.index(Z)
            elif hasattr(G, 'order') and hasattr(Z, 'order'):
                g_ord = G.order()
                z_ord = Z.order()
                if g_ord != sympy.oo:
                    index_Z = g_ord / z_ord
                elif z_ord == sympy.oo:
                    pass
                else:
                    index_Z = sympy.oo
        
        if index_Z is None:
            if hasattr(G, 'order') and G.order() == sympy.oo:
                raise ValueError("Cannot compute index of the center for infinite group without custom methods")
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            center_size = 0
            for g in elements:
                if all(g * h == h * g for h in elements):
                    center_size += 1
            index_Z = len(elements) / center_size

        if index_Z == sympy.oo or size_cl == sympy.oo:
            # In the context of infinite cardinals, integer divisibility fails
            neg_q = True
        else:
            size_cl_int = int(size_cl)
            index_Z_int = int(index_Z)
            if size_cl_int == 0:
                neg_q = True
            else:
                neg_q = (index_Z_int % size_cl_int != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G does not divide the index of the center of G"
]

N_HYP = 1
NEG_Q_INDEX = 1