import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                X = list(range(G.degree))
            elif len(witness) == 3:
                G, N, X = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and all(g in G for g in N.generators)
    except Exception:
        h2 = False

    # neg_Q: The operation is not well-defined or G/N is not a valid quotient group
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            try:
                is_normal = N.is_normal(G)
            except Exception:
                is_normal = True
                elements_G = list(G.generate_dimino())
                for g in N.generators:
                    for h in elements_G:
                        if (~h * g * h) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            elements_G = list(G.generate_dimino())
            elements_N = list(N.generate_dimino())
            
            def N_orbit(x):
                return frozenset(n(x) for n in elements_N)
            
            def left_coset(g):
                # In SymPy, n * g applies n then g, which corresponds to g(n(x)) in standard math.
                # This correctly generates the left coset gN.
                return frozenset(n * g for n in elements_N)
                
            cosets = set()
            for g in elements_G:
                cosets.add(left_coset(g))
                
            orbits = set()
            for x in X:
                orbits.add(N_orbit(x))
                
            well_defined = True
            for C in cosets:
                for O in orbits:
                    results = set()
                    for g_sym in C:
                        for x in O:
                            results.add(N_orbit(g_sym(x)))
                    if len(results) > 1:
                        well_defined = False
                        break
                if not well_defined:
                    break
            
            # The conclusion states the operation is well-defined AND forms a group action of G/N.
            # If N is not normal, G/N is not a group, so it fails.
            # If the operation is not well-defined, it also fails.
            neg_q = not (is_normal and well_defined)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a subgroup of G",
    "¬Q: The operation is not well-defined or does not form a group action of G/N"
]

N_HYP = 2
NEG_Q_INDEX = 2