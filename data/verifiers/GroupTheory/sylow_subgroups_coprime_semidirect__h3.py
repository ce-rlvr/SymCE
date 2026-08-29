import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
from sympy.ntheory import primefactors, isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Witness can be (G, N, H) or (G, N, H, p).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, N, H, p = witness
                p_list = [p]
            elif len(witness) == 3:
                G, N, H = witness
                p_list = primefactors(G.order())
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_subgroup(sub, group):
        for g in sub.generators:
            if not group.contains(g):
                return False
        return True

    def is_normal(sub, group):
        if not is_subgroup(sub, group):
            return False
        for g in group.generators:
            g_inv = g**-1
            for n in sub.generators:
                if not sub.contains(g * n * g_inv):
                    return False
        return True

    def trivial_intersection(N, H):
        if math.gcd(N.order(), H.order()) == 1:
            return True
        if N.order() < H.order():
            small, big = N, H
        else:
            small, big = H, N
        common = 0
        for g in small.generate():
            if big.contains(g):
                common += 1
                if common > 1:
                    return False
        return True

    # H_1: G = N \rtimes H is a finite semidirect product of groups N and H
    h1 = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if is_subgroup(N, G) and is_subgroup(H, G):
                if is_normal(N, G):
                    if N.order() * H.order() == G.order():
                        if trivial_intersection(N, H):
                            h1 = True
    except Exception:
        h1 = False

    # H_2: The orders |N| and |H| are relatively prime
    h2 = False
    try:
        if math.gcd(N.order(), H.order()) == 1:
            h2 = True
    except Exception:
        h2 = False

    def highest_power(prime, n):
        ans = 1
        while n > 0 and n % prime == 0:
            ans *= prime
            n //= prime
        return ans

    # ¬Q: There exists a prime p such that a Sylow p-subgroup of G is NOT isomorphic to a Sylow p-subgroup of H.
    # Since H <= G, the Sylow p-subgroup of H is isomorphic to a Sylow p-subgroup of G iff their orders are equal.
    neg_q = False
    try:
        for prime in p_list:
            if not isprime(prime):
                continue
            if highest_power(prime, G.order()) != highest_power(prime, H.order()):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semidirect product of N and H",
    "H_2: The orders |N| and |H| are relatively prime",
    "¬Q: There exists a prime p such that a Sylow p-subgroup of G is not isomorphic to a Sylow p-subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2