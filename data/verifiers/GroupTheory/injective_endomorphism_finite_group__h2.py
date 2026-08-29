import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_f(f, x):
    if isinstance(f, dict):
        return f[x]
    elif isinstance(f, (list, tuple)):
        for k, v in f:
            if k == x:
                return v
        raise ValueError("Mapping not found for element")
    return f(x)

def conditions(witness) -> list[bool]:
    try:
        G, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        elements = list(G.elements)
        e = G.identity
        h1_ok = getattr(G, 'is_finite', True) and len(elements) > 0
    except Exception:
        h1_ok = False

    # H_2: The kernel of f is the trivial subgroup {e_G}
    try:
        kernel = set()
        for x in elements:
            fx = get_f(f, x)
            if fx == e:
                kernel.add(x)
        h2_ok = (kernel == {e})
    except Exception:
        h2_ok = False

    # ¬Q: f is not an automorphism of G
    try:
        is_map = True
        for x in elements:
            fx = get_f(f, x)
            if fx not in elements:
                is_map = False
                break
        
        if not is_map:
            # If it doesn't map into G, it's not an automorphism
            neg_q_ok = True
        else:
            # Check if f is a bijection
            image = set()
            for x in elements:
                image.add(get_f(f, x))
            is_bijection = (len(image) == len(elements))
            
            # Check if f is a homomorphism
            is_homomorphism = True
            for x in elements:
                for y in elements:
                    fx = get_f(f, x)
                    fy = get_f(f, y)
                    fxy = get_f(f, x * y)
                    if fxy != fx * fy:
                        is_homomorphism = False
                        break
                if not is_homomorphism:
                    break
            
            is_automorphism = is_bijection and is_homomorphism
            neg_q_ok = not is_automorphism
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The kernel of f is the trivial subgroup {e_G}",
    "¬Q: f is not an automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2