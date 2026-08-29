import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy import oo
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    "H_1: N is a normal subgroup of G",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of xN in G/N does not divide the size of the conjugacy class of x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_orbit_size(G, x, N=None):
    orbit = [x]
    if hasattr(G, 'generators'):
        gens = G.generators
    elif hasattr(G, 'gens'):
        gens = G.gens
    else:
        gens = G
        
    for curr in orbit:
        for g in gens:
            try:
                nxt = g * curr * g**-1
            except Exception:
                try:
                    nxt = g * curr * ~g
                except Exception:
                    nxt = g * curr * g.inv()
                
            if N is None:
                if nxt not in orbit:
                    orbit.append(nxt)
            else:
                is_new = True
                for rep in orbit:
                    try:
                        diff = rep**-1 * nxt
                    except Exception:
                        try:
                            diff = ~rep * nxt
                        except Exception:
                            diff = rep.inv() * nxt
                        
                    if hasattr(N, 'contains'):
                        if N.contains(diff):
                            is_new = False
                            break
                    elif diff in N:
                        is_new = False
                        break
                if is_new:
                    orbit.append(nxt)
                    
        if len(orbit) > 2000:
            return float('inf')
            
    return len(orbit)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, N, x = witness
        else:
            G = witness.G
            N = witness.N
            x = witness.x
    except Exception:
        return [False, False, False]

    # H1: N is a normal subgroup of G
    try:
        if hasattr(N, 'is_normal'):
            if callable(N.is_normal):
                h1 = N.is_normal(G)
            else:
                h1 = N.is_normal
        elif hasattr(G, 'is_normal_subgroup'):
            h1 = G.is_normal_subgroup(N)
        else:
            h1 = True
            N_gens = N.generators if hasattr(N, 'generators') else (N.gens if hasattr(N, 'gens') else N)
            G_gens = G.generators if hasattr(G, 'generators') else (G.gens if hasattr(G, 'gens') else G)
            for n in N_gens:
                for g in G_gens:
                    try:
                        conj = g * n * g**-1
                    except Exception:
                        try:
                            conj = g * n * ~g
                        except Exception:
                            conj = g * n * g.inv()
                    if hasattr(N, 'contains'):
                        if not N.contains(conj):
                            h1 = False
                            break
                    elif conj not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h2 = G.contains(x)
        elif hasattr(G, '__contains__'):
            h2 = x in G
        else:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The size of the conjugacy class of xN in G/N does not divide the size of the conjugacy class of x in G
    try:
        if hasattr(witness, 'size_G') and hasattr(witness, 'size_GN'):
            size_G = witness.size_G
            size_GN = witness.size_GN
        else:
            if hasattr(G, 'conjugacy_class_size'):
                size_G = G.conjugacy_class_size(x)
            else:
                size_G = get_orbit_size(G, x)
                
            if hasattr(G, 'coset_conjugacy_class_size'):
                size_GN = G.coset_conjugacy_class_size(N, x)
            else:
                size_GN = get_orbit_size(G, x, N)
                
        if size_GN == 0:
            neg_q = True
        elif size_G in (float('inf'), oo) or size_GN in (float('inf'), oo):
            neg_q = True
        else:
            neg_q = (size_G % size_GN != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]