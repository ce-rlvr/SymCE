import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: x is an element of X",
    "¬Q: There is no bijection between the orbits of H on X and the double cosets H \\ G / G_x"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, H, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1_ok = bool(H.is_subgroup(G))
        else:
            h1_ok = all(g in G for g in H.generators)
    except Exception:
        h1_ok = False
        
    # H_2: x is an element of X
    try:
        h2_ok = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h2_ok = False
        
    # neg_Q: no bijection between orbits of H on X and double cosets H \ G / G_x
    try:
        def get_elements(group):
            if hasattr(group, 'elements'):
                return list(group.elements)
            return list(group.generate_dimino())
            
        # Compute orbits of H on X (where X is the domain of G)
        domain_size = G.degree
        elements = set(range(domain_size))
        orbits = []
        gens = H.generators
        while elements:
            start = elements.pop()
            orbit = {start}
            queue = [start]
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    try:
                        nxt = g(curr)
                    except Exception:
                        nxt = curr
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            elements -= orbit
            orbits.append(orbit)
        num_orbits = len(orbits)
        
        # Compute double cosets H \ G / G_x
        G_x = G.stabilizer(x)
        H_elems = get_elements(H)
        Gx_elems = get_elements(G_x)
        G_elems = get_elements(G)
        
        double_cosets = set()
        for g in G_elems:
            coset = frozenset(h * g * k for h in H_elems for k in Gx_elems)
            double_cosets.add(coset)
        num_double_cosets = len(double_cosets)
        
        neg_q_ok = (num_orbits != num_double_cosets)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]