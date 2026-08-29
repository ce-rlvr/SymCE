import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, isprime

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

def is_simple_group(S):
    if hasattr(S, 'is_simple'):
        val = S.is_simple
        if callable(val):
            return val()
        return val
    if hasattr(S, 'normal_subgroups'):
        return len(S.normal_subgroups()) == 2
    return False

def is_abelian_group(S):
    if hasattr(S, 'is_abelian'):
        val = S.is_abelian
        if callable(val):
            return val()
        return val
    return False

def is_normal_subgroup(G, S):
    for s in S.generators:
        if s not in G:
            return False
    for g in G.generators:
        for s in S.generators:
            if (~g * s * g) not in S:
                return False
    return True

def get_elements(G):
    if hasattr(G, 'elements'):
        return frozenset(G.elements)
    elif hasattr(G, 'generate_dimino'):
        return frozenset(G.generate_dimino())
    else:
        elements = set(G.generators)
        if hasattr(G, 'identity'):
            elements.add(G.identity)
        queue = list(elements)
        while queue:
            curr = queue.pop(0)
            for g in G.generators:
                nxt = curr * g
                if nxt not in elements:
                    elements.add(nxt)
                    queue.append(nxt)
        return frozenset(elements)

def count_sylow_p_subgroups(X, p):
    try:
        P = X.sylow_subgroup(p)
    except Exception:
        if X.order() % p != 0:
            return 1
        raise
        
    if P.order() == 1:
        return 1
    
    m = X.order() // P.order()
    possible_np = [k for k in range(1, m + 1, p) if m % k == 0]
    if len(possible_np) == 1:
        return possible_np[0]
        
    P_elements = get_elements(P)
    conjugates = set()
    conjugates.add(P_elements)
    
    queue = [P_elements]
    gens = X.generators
    while queue:
        curr = queue.pop(0)
        for g in gens:
            conj = frozenset(~g * x * g for x in curr)
            if conj not in conjugates:
                conjugates.add(conj)
                queue.append(conj)
    return len(conjugates)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, S_list, p = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a semisimple finite group such that G = S_1 x ... x S_k, where each S_i is a non-abelian simple group
    try:
        h1 = False
        if isinstance(S_list, list) and len(S_list) > 0:
            prod_order = 1
            for S in S_list:
                prod_order *= S.order()
            if G.order() == prod_order:
                h1 = True
                for S in S_list:
                    if S.order() <= 1 or is_abelian_group(S) or not is_simple_group(S):
                        h1 = False
                        break
                    if not is_normal_subgroup(G, S):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: p is a prime (n_p(X) denotes the number of Sylow p-subgroups)
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # neg_Q: The number of Sylow p-subgroups of G is NOT given by the product n_p(G) = \prod n_p(S_i)
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            np_G = count_sylow_p_subgroups(G, p)
            np_S_prod = 1
            for S in S_list:
                np_S_prod *= count_sylow_p_subgroups(S, p)
            neg_q = (np_G != np_S_prod)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group such that G = S_1 x ... x S_k, where each S_i is a non-abelian simple group",
    "H_2: n_p(X) denotes the number of Sylow p-subgroups of a finite group X (p is prime)",
    "¬Q: The number of Sylow p-subgroups of G is NOT given by the product n_p(G) = prod n_p(S_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2