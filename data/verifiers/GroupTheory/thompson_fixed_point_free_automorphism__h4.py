import sympy
from sympy.combinatorics import PermutationGroup
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

def apply_alpha(alpha, x):
    if isinstance(alpha, dict):
        return alpha.get(x, None)
    elif isinstance(alpha, list):
        for k, v in alpha:
            if k == x:
                return v
        return None
    else:
        return alpha(x)

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, alpha = witness
        else:
            G = witness.G
            alpha = witness.alpha
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: alpha is an automorphism of G
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        elements_set = set(elements)
        h2 = True
        mapped_elements = set()
        for x in elements:
            y = apply_alpha(alpha, x)
            if y not in elements_set:
                h2 = False
                break
            mapped_elements.add(y)
            
        if h2:
            if len(mapped_elements) != len(elements):
                h2 = False
            else:
                for x in elements:
                    for y in elements:
                        if apply_alpha(alpha, x * y) != apply_alpha(alpha, x) * apply_alpha(alpha, y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: alpha(x) = x implies x = e for all x in G
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        # Find the identity element
        identity = None
        for x in elements:
            is_id = True
            for y in elements:
                if x * y != y:
                    is_id = False
                    break
            if is_id:
                identity = x
                break
                
        h3 = True
        for x in elements:
            if apply_alpha(alpha, x) == x:
                if x != identity:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: G is not a nilpotent group
    try:
        if callable(G.is_nilpotent):
            neg_q = not G.is_nilpotent()
        else:
            neg_q = not G.is_nilpotent
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha is an automorphism of G",
    "H_3: alpha(x) = x implies x = e for all x in G",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 3
NEG_Q_INDEX = 3