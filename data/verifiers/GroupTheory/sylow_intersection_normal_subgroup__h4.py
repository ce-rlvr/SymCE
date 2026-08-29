import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def get_elements(G):
    """Safely extract elements from a group or iterable, removing duplicates."""
    if hasattr(G, 'generate'):
        elements = list(G.generate())
    elif hasattr(G, 'elements'):
        elements = list(G.elements)
    else:
        elements = list(G)
        
    unique_elements = []
    for e in elements:
        if e not in unique_elements:
            unique_elements.append(e)
    return unique_elements

def conditions(witness) -> list[bool]:
    try:
        G, p, N, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        G_elements = get_elements(G)
        h1 = len(G_elements) > 0
        if h1 and not isinstance(G, PermutationGroup):
            for a in G_elements:
                for b in G_elements:
                    if a * b not in G_elements:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        N_elements = get_elements(N)
        h3 = True
        for n in N_elements:
            if n not in G_elements:
                h3 = False
                break
        if h3 and len(N_elements) == 0:
            h3 = False
        elif h3:
            if not isinstance(N, PermutationGroup):
                for a in N_elements:
                    for b in N_elements:
                        if a * b not in N_elements:
                            h3 = False
                            break
                    if not h3:
                        break
            if h3:
                for g in G_elements:
                    try:
                        g_inv = g**-1
                    except Exception:
                        h3 = False
                        break
                    for n in N_elements:
                        if g * n * g_inv not in N_elements:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # ¬Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        P_elements = get_elements(P)
        intersection = [x for x in P_elements if x in N_elements]
        
        is_subgroup = True
        if len(intersection) == 0:
            is_subgroup = False
        else:
            for a in intersection:
                for b in intersection:
                    if a * b not in intersection:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
        
        if not is_subgroup:
            is_sylow = False
        else:
            n_order = len(N_elements)
            target_size = 1
            if isinstance(p, (int, sympy.Integer)) and p > 1:
                temp = n_order
                while temp % p == 0:
                    target_size *= p
                    temp //= p
            is_sylow = (len(intersection) == target_size)
            
        neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is a normal subgroup of G",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3