import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(G):
    try:
        _ = G.identity
        if hasattr(G, 'generate'):
            _ = list(G.generate())
        elif hasattr(G, 'elements'):
            _ = list(G.elements)
        else:
            return False
        return True
    except Exception:
        return False

def get_elements(G):
    if hasattr(G, 'generate'):
        return list(G.generate())
    elif hasattr(G, 'elements'):
        return list(G.elements)
    else:
        return list(G)

def evaluate_func(func, x):
    if callable(func):
        return func(x)
    return func[x]

def is_homomorphism(G, H, func):
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        for x in G_elems:
            fx = evaluate_func(func, x)
            if fx not in H_elems:
                return False
        for x in G_elems:
            for y in G_elems:
                f_xy = evaluate_func(func, x * y)
                fx = evaluate_func(func, x)
                fy = evaluate_func(func, y)
                if f_xy != fx * fy:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        H1 = witness['H1']
        H2 = witness['H2']
        f = witness['f']
        g = witness['g']
        phi = witness['phi']
    except Exception:
        return [False, False, False, False]

    # H1: G, H1, H2 are groups
    try:
        h1_ok = is_group(G) and is_group(H1) and is_group(H2)
    except Exception:
        h1_ok = False

    # H2: f is a homomorphism from G to H1
    try:
        h2_ok = is_homomorphism(G, H1, f)
    except Exception:
        h2_ok = False

    # H3: g is a homomorphism from G to H2
    try:
        h3_ok = is_homomorphism(G, H2, g)
    except Exception:
        h3_ok = False

    # ¬Q: ker(phi) != ker(f) \cap ker(g)
    try:
        G_elems = get_elements(G)
        ker_f = {x for x in G_elems if evaluate_func(f, x) == H1.identity}
        ker_g = {x for x in G_elems if evaluate_func(g, x) == H2.identity}
        
        # The kernel of phi is the preimage of the identity of its codomain.
        # Assuming phi is a homomorphism, phi(G.identity) is that identity.
        e_K = evaluate_func(phi, G.identity)
        ker_phi = {x for x in G_elems if evaluate_func(phi, x) == e_K}
        
        conclusion = (ker_phi == ker_f.intersection(ker_g))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G, H_1, and H_2 are groups",
    "H_2: f is a group homomorphism from G to H_1",
    "H_3: g is a group homomorphism from G to H_2",
    "¬Q: The kernel of phi is not equal to ker(f) ∩ ker(g)"
]

N_HYP = 3
NEG_Q_INDEX = 3