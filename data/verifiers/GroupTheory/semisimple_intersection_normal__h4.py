import sympy
from sympy.combinatorics import PermutationGroup, Permutation, AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        N1 = witness.get('N1')
        N2 = witness.get('N2')
    else:
        try:
            G, N1, N2 = witness
        except Exception:
            return [False, False, False, False]
            
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G is isomorphic to a direct product of non-abelian simple groups
    try:
        h2 = False
        if G.order() > 1:
            cs = G.composition_series()
            h2 = True
            for i in range(len(cs) - 1):
                factor_order = cs[i].order() // cs[i+1].order()
                if sympy.isprime(factor_order):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: N_1 is a normal subgroup of G
    try:
        h3 = True
        max_size_G = max(G.degree, N1.degree)
        def pad_G(p, size):
            if p.size >= size:
                return p
            arr = p.array_form
            arr.extend(list(range(len(arr), size)))
            return Permutation(arr)
            
        G_gens = [pad_G(p, max_size_G) for p in G.generators]
        N1_gens = [pad_G(p, max_size_G) for p in N1.generators]
        
        G_pad = PermutationGroup(G_gens)
        N1_pad = PermutationGroup(N1_gens)
        
        for h in N1_gens:
            if not G_pad.contains(h):
                h3 = False
                break
                
        if h3:
            for g in G_gens:
                for h in N1_gens:
                    if not N1_pad.contains(g * h * ~g):
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: N_1 \cap N_2 is neither trivial nor a direct product of non-abelian simple groups
    try:
        neg_q = False
        max_size_N = max(N1.degree, N2.degree)
        def pad_N(p, size):
            if p.size >= size:
                return p
            arr = p.array_form
            arr.extend(list(range(len(arr), size)))
            return Permutation(arr)
            
        elems_N1 = set(pad_N(p, max_size_N) for p in N1.generate())
        elems_N2 = set(pad_N(p, max_size_N) for p in N2.generate())
        intersect_elems = list(elems_N1.intersection(elems_N2))
        
        if not intersect_elems:
            neg_q = False
        else:
            N12 = PermutationGroup(intersect_elems)
            
            if N12.order() == 1:
                neg_q = False
            else:
                is_dp = True
                cs_N12 = N12.composition_series()
                for i in range(len(cs_N12) - 1):
                    factor_order = cs_N12[i].order() // cs_N12[i+1].order()
                    if sympy.isprime(factor_order):
                        is_dp = False
                        break
                neg_q = not is_dp
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is isomorphic to a direct product of non-abelian simple groups",
    "H_3: N_1 is a normal subgroup of G",
    "¬Q: N_1 \\cap N_2 is neither the trivial subgroup nor isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 3
NEG_Q_INDEX = 3