import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math

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

def conditions(witness) -> list[bool]:
    try:
        G, N, H, p = witness
    except Exception:
        return [False] * 5

    # H1: G is a group, and N and H are subgroups of G
    try:
        h1 = bool(N.is_subgroup(G) and H.is_subgroup(G))
    except Exception:
        h1 = False

    # H2: The orders of N and H are relatively prime
    try:
        h2 = math.gcd(int(N.order()), int(H.order())) == 1
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(sympy.isprime(p))
    except Exception:
        h3 = False

    # H4: p divides the order of H
    try:
        h4 = int(H.order()) % int(p) == 0
    except Exception:
        h4 = False

    # neg_Q: There exists a Sylow p-subgroup of G that is not conjugate to a Sylow p-subgroup of H
    # This happens if and only if the highest power of p dividing |G| is strictly greater than
    # the highest power of p dividing |H|.
    try:
        def p_part(n, p):
            count = 0
            while n > 0 and n % p == 0:
                count += 1
                n //= p
            return count
        
        a = p_part(int(G.order()), int(p))
        b = p_part(int(H.order()), int(p))
        neg_q = bool(a > b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group, and N and H are subgroups of G",
    "H_2: The orders of N and H are relatively prime",
    "H_3: p is a prime number",
    "H_4: p divides the order of H",
    "¬Q: There exists a Sylow p-subgroup of G that is not conjugate to a Sylow p-subgroup of H"
]

N_HYP = 4
NEG_Q_INDEX = 4