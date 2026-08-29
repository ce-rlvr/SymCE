import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
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

def count_automorphisms_manual(N):
    """
    Counts the number of automorphisms of a finite permutation group N
    by checking all possible assignments of its generators.
    """
    gens = N.generators
    elements = list(N.generate())
    id_elem = N.identity
    aut_count = 0
    
    for images in itertools.product(elements, repeat=len(gens)):
        full_map = {id_elem: id_elem}
        frontier = [id_elem]
        valid = True
        
        while frontier and valid:
            curr = frontier.pop(0)
            for g, img in zip(gens, images):
                nxt = curr * g
                nxt_img = full_map[curr] * img
                if nxt in full_map:
                    if full_map[nxt] != nxt_img:
                        valid = False
                        break
                else:
                    full_map[nxt] = nxt_img
                    frontier.append(nxt)
                    
        if valid and len(full_map) == N.order():
            aut_count += 1
            
    return aut_count

def is_complete(N):
    """
    Checks if N is a complete group (trivial center and every automorphism is inner).
    Since the center is trivial, it is complete iff |Aut(N)| == |N|.
    """
    try:
        if N.center().order() != 1:
            return False
        
        order = N.order()
        # Fast paths for common complete groups
        if order == 6 and N.is_isomorphic(SymmetricGroup(3)):
            return True
        if order == 24 and N.is_isomorphic(SymmetricGroup(4)):
            return True
            
        aut_count = count_automorphisms_manual(N)
        return aut_count == order
    except Exception:
        return False

def is_normal_subgroup(H, G):
    """
    Checks if H is a normal subgroup of G.
    """
    try:
        h_elements = set(H.generate())
        g_elements = set(G.generate())
        if not h_elements.issubset(g_elements):
            return False
        for g in G.generators:
            g_inv = g**-1
            for h in H.generators:
                if g * h * g_inv not in h_elements:
                    return False
        return True
    except Exception:
        return False

def centralizer(G, N):
    """
    Returns the centralizer C_G(N) as a PermutationGroup.
    """
    c_elements = []
    n_gens = N.generators
    for g in G.generate():
        if all(g * n == n * g for n in n_gens):
            c_elements.append(g)
    if not c_elements:
        return PermutationGroup([G.identity])
    return PermutationGroup(c_elements)

def is_internal_direct_product(G, N, C):
    """
    Checks if G is the internal direct product of N and C.
    """
    try:
        if not is_normal_subgroup(N, G):
            return False
        if not is_normal_subgroup(C, G):
            return False
        n_elements = set(N.generate())
        c_elements = set(C.generate())
        if len(n_elements.intersection(c_elements)) != 1:
            return False
        if N.order() * C.order() != G.order():
            return False
        return True
    except Exception:
        return False

def check_isomorphic(H, C):
    try:
        return H.is_isomorphic(C)
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness (G, N, H), checks the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, N, H = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'N') and hasattr(witness, 'H'):
            G = witness.G
            N = witness.N
            H = witness.H
        elif isinstance(witness, dict) and 'G' in witness and 'N' in witness and 'H' in witness:
            G = witness['G']
            N = witness['N']
            H = witness['H']
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: N is a complete group
    try:
        h1_ok = is_complete(N)
    except Exception:
        h1_ok = False

    # neg_Q: H is not isomorphic to C_G(N) or G is not the internal direct product of N and C_G(N)
    try:
        C = centralizer(G, N)
        iso = check_isomorphic(H, C)
        idp = is_internal_direct_product(G, N, C)
        neg_q_ok = not (iso and idp)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a complete group",
    "¬Q: H is not isomorphic to C_G(N) or G is not the internal direct product of N and C_G(N)"
]

N_HYP = 1
NEG_Q_INDEX = 1