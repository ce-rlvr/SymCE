import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_k(G):
    elements = list(G.generate())
    seen = set()
    k = 0
    for x in elements:
        if x not in seen:
            c = set(g * x * ~g for g in elements)
            seen.update(c)
            k += 1
    return k

def get_k_quotient(G, N):
    elements = list(G.generate())
    N_elements = list(N.generate())
    
    cosets = []
    element_to_coset = {}
    for x in elements:
        if x not in element_to_coset:
            c = frozenset(x * n for n in N_elements)
            cosets.append(c)
            for y in c:
                element_to_coset[y] = c
                
    seen_cosets = set()
    k_q = 0
    for c in cosets:
        if c not in seen_cosets:
            x = next(iter(c))
            conj_class = set()
            for g in elements:
                target = g * x * ~g
                if target in element_to_coset:
                    conj_class.add(element_to_coset[target])
            seen_cosets.update(conj_class)
            k_q += 1
    return k_q

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
        elif len(witness) >= 2:
            G, N = witness[0], witness[1]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = hasattr(G, 'generate') and hasattr(G, 'order') and G.order() > 0
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        if hasattr(N, 'generate') and hasattr(N, 'generators'):
            N_elements = set(N.generate())
            G_elements = set(G.generate())
            is_subgroup = N_elements.issubset(G_elements)
            
            is_normal = True
            if is_subgroup:
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N_elements:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            h2 = is_subgroup and is_normal
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: k(G) is the number of conjugacy classes of G
    try:
        k_G = get_k(G)
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: k(G/N) <= k(G) fails, so k(G/N) > k(G)
    try:
        k_G = get_k(G)
        k_q = get_k_quotient(G, N)
        neg_q = k_q > k_G
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: k(G) is the number of conjugacy classes of G",
    "¬Q: k(G/N) > k(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3