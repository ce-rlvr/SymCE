import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
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

def apply_alpha(alpha, g):
    if isinstance(alpha, dict):
        return alpha[g]
    elif callable(alpha):
        return alpha(g)
    else:
        raise ValueError("alpha must be a dict or callable")

def conditions(witness) -> list[bool]:
    try:
        G, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: alpha is an automorphism of G
    try:
        elements = list(G.generate())
        mapped_elements = [apply_alpha(alpha, g) for g in elements]
        
        # Check bijection
        if len(set(mapped_elements)) != len(elements):
            h2 = False
        elif not all(m in elements for m in mapped_elements):
            h2 = False
        else:
            # Check homomorphism property
            h2 = True
            for x in elements:
                for y in elements:
                    if apply_alpha(alpha, x * y) != apply_alpha(alpha, x) * apply_alpha(alpha, y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: The order of alpha is a prime number
    try:
        elements = list(G.generate())
        idx_map = {g: i for i, g in enumerate(elements)}
        perm = [idx_map[apply_alpha(alpha, g)] for g in elements]
        p = Permutation(perm)
        order = p.order()
        h3 = bool(isprime(order))
    except Exception:
        h3 = False

    # ¬Q: G is not a nilpotent group
    try:
        is_nilp = G.is_nilpotent
        if callable(is_nilp):
            is_nilp = is_nilp()
        neg_q = not bool(is_nilp)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha is an automorphism of G",
    "H_3: The order of alpha is a prime number",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 3
NEG_Q_INDEX = 3