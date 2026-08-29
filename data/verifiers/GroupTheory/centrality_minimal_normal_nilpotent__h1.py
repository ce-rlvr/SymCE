import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]

    # H1: N is a minimal normal subgroup of G
    try:
        def is_subgroup(H, Grp):
            for h in H.generators:
                if not Grp.contains(h):
                    return False
            return True

        def is_normal(Grp, H):
            if not is_subgroup(H, Grp):
                return False
            for g in Grp.generators:
                for h in H.generators:
                    if not H.contains(g * h * ~g):
                        return False
            return True

        def is_minimal_normal(Grp, H):
            if H.order() == 1:
                return False
            if not is_normal(Grp, H):
                return False
            
            # For a normal subgroup H to be minimal, the normal closure in Grp 
            # of any non-identity element x in H must be equal to H.
            for x in H.generate():
                if x.is_Identity:
                    continue
                
                # Compute the normal closure of x in Grp
                C = {x}
                queue = [x]
                gens = Grp.generators
                while queue:
                    curr = queue.pop(0)
                    for g in gens:
                        conj = g * curr * ~g
                        if conj not in C:
                            C.add(conj)
                            queue.append(conj)
                
                NC = PermutationGroup(*list(C))
                if NC.order() < H.order():
                    return False
            return True

        h1_ok = bool(is_minimal_normal(G, N))
    except Exception:
        h1_ok = False

    # neg_Q: N is NOT contained in the center of G
    try:
        def in_center(Grp, H):
            for h in H.generators:
                for g in Grp.generators:
                    if h * g != g * h:
                        return False
            return True

        neg_q_ok = not bool(in_center(G, N))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a minimal normal subgroup of G",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 1
NEG_Q_INDEX = 1