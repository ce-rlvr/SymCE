import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: N is an abelian normal subgroup of G",
    "H_2: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "H_3: n1 and n2 are elements of N",
    "¬Q: n1 and n2 are conjugate in G iff they are conjugate by an element of H (fails)"
]

def conditions(witness):
    try:
        if len(witness) != 5:
            return [False, False, False, False]
        G, N, H, n1, n2 = witness
    except Exception:
        return [False, False, False, False]

    # H_1: N is an abelian normal subgroup of G
    try:
        N_is_subgroup = all(G.contains(gen) for gen in N.generators)
        
        N_is_abelian = True
        for g1 in N.generators:
            for g2 in N.generators:
                if g1 * g2 != g2 * g1:
                    N_is_abelian = False
                    break
            if not N_is_abelian:
                break
                
        N_is_normal = True
        if N_is_subgroup:
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * (~g)):
                        N_is_normal = False
                        break
                    if not N.contains((~g) * n * g):
                        N_is_normal = False
                        break
                if not N_is_normal:
                    break
        else:
            N_is_normal = False
            
        h1 = N_is_subgroup and N_is_abelian and N_is_normal
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G such that G is the internal semidirect product of N and H
    try:
        H_is_subgroup = all(G.contains(gen) for gen in H.generators)
        
        intersect_trivial = True
        for n in N.generate():
            if n.is_Identity:
                continue
            if H.contains(n):
                intersect_trivial = False
                break
                
        order_cond = (N.order() * H.order() == G.order())
        
        h2 = H_is_subgroup and intersect_trivial and order_cond
    except Exception:
        h2 = False

    # H_3: n1 and n2 are elements of N
    try:
        h3 = N.contains(n1) and N.contains(n2)
    except Exception:
        h3 = False

    # ¬Q: Conclusion fails (n1 and n2 are conjugate in G iff there exists h in H such that h n1 h^-1 = n2)
    try:
        P = False
        for g in G.generate():
            if g * n1 * (~g) == n2:
                P = True
                break
                
        Q = False
        for h in H.generate():
            if h * n1 * (~h) == n2:
                Q = True
                break
                
        neg_Q = (P != Q)
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]