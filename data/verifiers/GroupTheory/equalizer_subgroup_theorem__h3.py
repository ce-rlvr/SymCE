import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            g = witness.get('g')
        elif isinstance(witness, tuple) and len(witness) == 4:
            G, H, f, g = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def apply_map(m, x):
        if isinstance(m, dict):
            return m[x]
        else:
            return m(x)

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f is a group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            G_elems = list(G.generate())
            H_elems = list(H.generate())
            for x in G_elems:
                fx = apply_map(f, x)
                if fx not in H_elems:
                    h2 = False
                    break
                for y in G_elems:
                    fy = apply_map(f, y)
                    fxy = apply_map(f, x * y)
                    if fxy != fx * fy:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: E = {x in G | f(x) = g(x)} is NOT a subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            E = set()
            G_elems = list(G.generate())
            for x in G_elems:
                fx = apply_map(f, x)
                gx = apply_map(g, x)
                if fx == gx:
                    E.add(x)
            
            is_subgroup = True
            if not E:
                is_subgroup = False
            else:
                ident = None
                for e in E:
                    if e * e == e:
                        ident = e
                        break
                if ident is None:
                    is_subgroup = False
                else:
                    for x in E:
                        if ~x not in E:
                            is_subgroup = False
                            break
                        for y in E:
                            if x * y not in E:
                                is_subgroup = False
                                break
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: E = {x \\in G \\mid f(x) = g(x)} is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2