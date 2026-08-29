import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the conjecture.
    Witness should be a tuple: (G, H1, H2, f, g) or (G, H1, H2, f, g, phi)
    where f, g, phi are dictionaries or callables mapping elements.
    """
    try:
        if len(witness) == 5:
            G, H1, H2, f, g = witness
            phi = None
        elif len(witness) == 6:
            G, H1, H2, f, g, phi = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def apply_map(m, x):
        if isinstance(m, dict):
            return m[x]
        return m(x)

    # Extract elements and identities
    try:
        G_elems = list(G.elements)
        H1_elems = list(H1.elements)
        id_H1 = H1.identity
    except Exception:
        G_elems = []
        H1_elems = []
        id_H1 = None

    try:
        H2_elems = list(H2.elements)
        id_H2 = H2.identity
    except Exception:
        H2_elems = []
        id_H2 = None

    # H1: f is a group homomorphism from G to H1
    try:
        h1_ok = True
        if not G_elems or not H1_elems:
            h1_ok = False
        for x in G_elems:
            fx = apply_map(f, x)
            if fx not in H1_elems:
                h1_ok = False
                break
            for y in G_elems:
                fy = apply_map(f, y)
                fxy = apply_map(f, x * y)
                if fxy != fx * fy:
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    # H2: g is a group homomorphism from G to H2
    try:
        h2_ok = True
        if not G_elems or not H2_elems:
            h2_ok = False
        for x in G_elems:
            gx = apply_map(g, x)
            if gx not in H2_elems:
                h2_ok = False
                break
            for y in G_elems:
                gy = apply_map(g, y)
                gxy = apply_map(g, x * y)
                if gxy != gx * gy:
                    h2_ok = False
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # H3: phi is defined by phi(x) = (f(x), g(x))
    try:
        h3_ok = True
        for x in G_elems:
            fx = apply_map(f, x)
            gx = apply_map(g, x)
            if phi is not None:
                phix = apply_map(phi, x)
                if phix != (fx, gx):
                    h3_ok = False
                    break
    except Exception:
        h3_ok = False

    # ¬Q: The kernel of phi is NOT equal to ker(f) \cap ker(g)
    try:
        ker_f = set()
        ker_g = set()
        ker_phi = set()
        
        for x in G_elems:
            fx = apply_map(f, x)
            gx = apply_map(g, x)
            
            if fx == id_H1:
                ker_f.add(x)
            if gx == id_H2:
                ker_g.add(x)
            
            if phi is not None:
                phix = apply_map(phi, x)
                if phix == (id_H1, id_H2):
                    ker_phi.add(x)
            else:
                if fx == id_H1 and gx == id_H2:
                    ker_phi.add(x)
                
        conclusion = (ker_phi == ker_f.intersection(ker_g))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H_1",
    "H_2: g is a group homomorphism from G to H_2",
    "H_3: phi is defined by phi(x) = (f(x), g(x))",
    "¬Q: The kernel of phi is not equal to ker(f) intersection ker(g)"
]

N_HYP = 3
NEG_Q_INDEX = 3