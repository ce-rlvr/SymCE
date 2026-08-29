import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime, factorint
import itertools
import functools
import math

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N, H, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group that is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup) or not isinstance(H, PermutationGroup):
            h1 = False
        else:
            if not all(g in G for g in N.generators):
                h1 = False
            elif not all(g in G for g in H.generators):
                h1 = False
            elif not N.is_normal(G):
                h1 = False
            else:
                n_elems = set(N.generate())
                h_elems = set(H.generate())
                intersection = n_elems.intersection(h_elems)
                if len(intersection) != 1:
                    h1 = False
                elif N.order() * H.order() != G.order():
                    h1 = False
                else:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: N is an abelian p-group
    try:
        if not N.is_abelian:
            h3 = False
        else:
            order = N.order()
            if order == 1:
                h3 = True
            else:
                factors = factorint(order)
                if len(factors) == 1 and p in factors:
                    h3 = True
                else:
                    h3 = False
    except Exception:
        h3 = False

    # neg_Q: N is NOT the internal direct product of C_N(H) and the mixed commutator subgroup
    try:
        n_elems = list(N.generate())
        h_elems = list(H.generate())
        
        c_n_h = []
        for n in n_elems:
            if all(n * h == h * n for h in h_elems):
                c_n_h.append(n)
                
        commutators = []
        for n in n_elems:
            for h in h_elems:
                c = (~n) * (~h) * n * h
                commutators.append(c)
                
        comm_subgroup = PermutationGroup(commutators)
        comm_elems = set(comm_subgroup.generate())
        c_n_h_elems = set(c_n_h)
        
        intersection = c_n_h_elems.intersection(comm_elems)
        
        if len(intersection) != 1:
            is_direct_product = False
        elif len(c_n_h_elems) * len(comm_elems) != N.order():
            is_direct_product = False
        else:
            is_direct_product = True
            
        neg_q = not is_direct_product
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group that is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: p is a prime number",
    "H_3: N is an abelian p-group",
    "¬Q: N is not the internal direct product of C_N(H) and the mixed commutator subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3