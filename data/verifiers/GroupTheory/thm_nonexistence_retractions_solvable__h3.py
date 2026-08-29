import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, S = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a semisimple finite group
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            elements = list(G.generate())
            if not elements:
                h1 = True
            else:
                h1 = True
                id_elem = elements[0] * ~elements[0]
                for x in elements:
                    if x == id_elem:
                        continue
                    
                    # Compute the normal closure of x in G
                    closure_gens = {x}
                    queue = [x]
                    while queue:
                        curr = queue.pop(0)
                        for g in G.generators:
                            conj = g * curr * ~g
                            if conj not in closure_gens:
                                closure_gens.add(conj)
                                queue.append(conj)
                    
                    N = PermutationGroup(list(closure_gens))
                    is_solv = N.is_solvable
                    if callable(is_solv):
                        is_solv = is_solv()
                    
                    # A finite group is semisimple iff it has no non-trivial solvable normal subgroups
                    if is_solv:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: S is a solvable subgroup of G
    try:
        if not isinstance(S, PermutationGroup):
            h2 = False
        else:
            is_subgroup = True
            for g in S.generators:
                if g not in G:
                    is_subgroup = False
                    break
            
            is_solv = S.is_solvable
            if callable(is_solv):
                is_solv = is_solv()
                
            h2 = is_subgroup and bool(is_solv)
    except Exception:
        h2 = False

    # ¬Q: S is not the trivial subgroup
    try:
        neg_q = len(list(S.generate())) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: S is a solvable subgroup of G",
    "¬Q: S is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2