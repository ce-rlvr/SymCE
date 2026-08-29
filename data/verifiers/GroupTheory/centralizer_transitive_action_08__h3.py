import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import math
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

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G is a subgroup of the symmetric group Sym(X)",
    "H_3: C is the centralizer of G in Sym(X)",
    "¬Q: C does not act semi-regularly on X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, C = witness
            if isinstance(G, PermutationGroup) and isinstance(C, PermutationGroup):
                degree = max(G.degree, C.degree)
                h1 = True
                h2 = True
                
                is_cent = True
                for g in G.generators:
                    for c in C.generators:
                        if g * c != c * g:
                            is_cent = False
                            break
                    if not is_cent:
                        break
                
                if is_cent:
                    if degree <= 6:
                        count = 0
                        for p in itertools.permutations(range(degree)):
                            perm = Permutation(list(p))
                            commutes = True
                            for g in G.generators:
                                if perm * g != g * perm:
                                    commutes = False
                                    break
                            if commutes:
                                count += 1
                        if count == C.order():
                            h3 = True
                    else:
                        S = SymmetricGroup(degree)
                        C_actual = S.centralizer(G)
                        if C.order() == C_actual.order():
                            h3 = True
                            
        elif isinstance(witness, PermutationGroup):
            G = witness
            degree = G.degree
            h1 = True
            h2 = True
            
            C_gens = []
            if degree <= 6:
                for p in itertools.permutations(range(degree)):
                    perm = Permutation(list(p))
                    commutes = True
                    for g in G.generators:
                        if perm * g != g * perm:
                            commutes = False
                            break
                    if commutes:
                        C_gens.append(perm)
                C = PermutationGroup(C_gens)
                h3 = True
            else:
                S = SymmetricGroup(degree)
                C = S.centralizer(G)
                h3 = True
    except Exception:
        pass

    try:
        if h1 and h2 and h3:
            for c in list(C.generate()):
                # Check if c is the identity permutation
                is_id = True
                for x in range(degree):
                    if c(x) != x:
                        is_id = False
                        break
                if is_id:
                    continue
                
                # Check if c has any fixed points
                has_fixed = False
                for x in range(degree):
                    if c(x) == x:
                        has_fixed = True
                        break
                
                if has_fixed:
                    neg_q = True
                    break
    except Exception:
        pass

    return [h1, h2, h3, neg_q]