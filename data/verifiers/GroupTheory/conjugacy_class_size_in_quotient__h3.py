import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # witness can be (G, N) or (G, N, g)
    try:
        if len(witness) == 3:
            G, N, g = witness
            g_list = [g]
        elif len(witness) == 2:
            G, N = witness
            try:
                g_list = list(G.elements)
            except Exception:
                g_list = list(G.generate())
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        if h1 and isinstance(N, PermutationGroup):
            is_sub = True
            for n_gen in N.generators:
                if not G.contains(n_gen):
                    is_sub = False
                    break
            
            if is_sub:
                h2 = True
                for g_gen in G.generators:
                    for n_gen in N.generators:
                        if not N.contains(g_gen * n_gen * ~g_gen):
                            h2 = False
                            break
                        if not N.contains(~g_gen * n_gen * g_gen):
                            h2 = False
                            break
                    if not h2:
                        break
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The size of the conjugacy class of gN in G/N does not divide the size of the conjugacy class of g in G
    neg_q = False
    try:
        if h1 and h2:
            for g_test in g_list:
                if not G.contains(g_test):
                    continue
                
                # Compute orbit of g_test in G (conjugacy class of g in G)
                orbit = {g_test}
                q = [g_test]
                gens = G.generators
                while q:
                    curr = q.pop(0)
                    for gen in gens:
                        nxt = gen * curr * ~gen
                        if nxt not in orbit:
                            orbit.add(nxt)
                            q.append(nxt)
                size_g = len(orbit)
                
                # Compute unique cosets in the orbit (conjugacy class of gN in G/N)
                unique_cosets = []
                for h in orbit:
                    found = False
                    for rep in unique_cosets:
                        # Check if h is in the same left coset as rep: rep^-1 * h in N
                        if N.contains(~rep * h):
                            found = True
                            break
                    if not found:
                        unique_cosets.append(h)
                size_gN = len(unique_cosets)
                
                # Check if the conclusion fails
                if size_gN == 0 or size_g % size_gN != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The size of the conjugacy class of gN in G/N does not divide the size of the conjugacy class of g in G"
]

N_HYP = 2
NEG_Q_INDEX = 2