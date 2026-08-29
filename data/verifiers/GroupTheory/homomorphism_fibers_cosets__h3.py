import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def apply_f(f, x):
    if callable(f):
        return f(x)
    return f[x]

def in_group(x, grp):
    if isinstance(grp, PermutationGroup):
        return grp.contains(x)
    return x in list(grp.elements)

def get_identity(group):
    if hasattr(group, 'identity'):
        return group.identity
    elements = list(group.elements)
    if not elements:
        raise ValueError("Empty group")
    e = elements[0]
    return e * e**-1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            x = witness['x']
            y = witness['y']
        else:
            G, H, f, x, y = witness
    except Exception:
        return [False, False, False]

    # H1: G and H are groups
    h1 = False
    try:
        for group in (G, H):
            if not hasattr(group, 'elements'):
                raise ValueError
            
            elements = list(group.elements)
            if not elements:
                raise ValueError
                
            identity = get_identity(group)
            
            if not isinstance(group, PermutationGroup):
                if len(elements) > 1000:
                    raise ValueError
                if identity not in elements:
                    raise ValueError
                for a in elements:
                    if a**-1 not in elements:
                        raise ValueError
                    for b in elements:
                        if a * b not in elements:
                            raise ValueError
        h1 = True
    except Exception:
        h1 = False

    # H2: f is a group homomorphism
    h2 = False
    try:
        if h1:
            is_hom = True
            for g in G.elements:
                val = apply_f(f, g)
                if not in_group(val, H):
                    is_hom = False
                    break
            if is_hom:
                for g1 in G.elements:
                    for g2 in G.elements:
                        val1 = apply_f(f, g1 * g2)
                        val2 = apply_f(f, g1) * apply_f(f, g2)
                        if val1 != val2:
                            is_hom = False
                            break
                    if not is_hom:
                        break
            h2 = is_hom
    except Exception:
        h2 = False

    # neg_Q: f(x) = f(y) if and only if x^{-1}y \in \ker(f) FAILS
    neg_q = False
    try:
        H_id = get_identity(H)
        ker_f = []
        for g in G.elements:
            if apply_f(f, g) == H_id:
                ker_f.append(g)
        
        fx = apply_f(f, x)
        fy = apply_f(f, y)
        left_side = (fx == fy)
        
        x_inv_y = (x**-1) * y
        right_side = (x_inv_y in ker_f)
        
        neg_q = (left_side != right_side)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: f(x) = f(y) if and only if x^{-1}y \\in \\ker(f) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2