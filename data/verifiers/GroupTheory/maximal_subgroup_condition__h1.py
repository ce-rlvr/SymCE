import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
        G, N, H = witness
    except Exception:
        return [False, False, False]

    def is_subgroup(sub, grp):
        for gen in sub.generators:
            if gen not in grp:
                return False
        return True

    def is_normal(sub, grp):
        if not is_subgroup(sub, grp): 
            return False
        for n in sub.generators:
            for g in grp.generators:
                if g * n * ~g not in sub:
                    return False
                if ~g * n * g not in sub:
                    return False
        return True

    # H1: N is an abelian group
    try:
        h1 = bool(N.is_abelian)
    except Exception:
        h1 = False

    # H2: N is a minimal normal subgroup of G
    try:
        h2 = False
        if is_normal(N, G) and N.order() > 1:
            h2 = True
            for x in N.generate():
                if not x.is_Identity:
                    orbit = {x}
                    queue = [x]
                    idx = 0
                    while idx < len(queue):
                        curr = queue[idx]
                        idx += 1
                        for g in G.generators:
                            conj = g * curr * ~g
                            if conj not in orbit:
                                orbit.add(conj)
                                queue.append(conj)
                            conj_inv = ~g * curr * g
                            if conj_inv not in orbit:
                                orbit.add(conj_inv)
                                queue.append(conj_inv)
                    closure = PermutationGroup(list(orbit))
                    if closure.order() < N.order():
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: H is NOT a maximal subgroup of G
    try:
        def is_maximal_subgroup(sub, grp):
            if not is_subgroup(sub, grp):
                return False
            if sub.order() == grp.order():
                return False
            for g in grp.generate():
                if g not in sub:
                    gens = list(sub.generators) + [g]
                    M = PermutationGroup(gens)
                    if M.order() < grp.order():
                        return False
            return True

        neg_q = not is_maximal_subgroup(H, G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is an abelian group",
    "H_2: N is a minimal normal subgroup of G",
    "¬Q: H is not a maximal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2