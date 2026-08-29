import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.ntheory import isprime

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

def p_part(n, p):
    if p <= 1 or n == 0:
        return 1
    ans = 1
    while n % p == 0:
        ans *= p
        n //= p
    return ans

def is_subgroup(sub, group):
    try:
        return all(group.contains(g) for g in sub.generators)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        A, B, p, P, Q = witness
    except Exception:
        return [False] * 6

    # H_1: p is a prime
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: p divides the order of A
    try:
        A_order = A.order()
        h2 = (A_order % p == 0)
    except Exception:
        h2 = False

    # H_3: p divides the order of B
    try:
        B_order = B.order()
        h3 = (B_order % p == 0)
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of A
    try:
        P_order = P.order()
        h4 = (P_order == p_part(A_order, p)) and is_subgroup(P, A)
    except Exception:
        h4 = False

    # H_5: Q is a Sylow p-subgroup of B
    try:
        Q_order = Q.order()
        h5 = (Q_order == p_part(B_order, p)) and is_subgroup(Q, B)
    except Exception:
        h5 = False

    # ¬Q: P \wr Q is not isomorphic to a Sylow p-subgroup of A \wr B
    try:
        # The order of the standard wreath product P \wr Q is |P|^|Q| * |Q|
        wreath_PQ_order = (P_order ** Q_order) * Q_order
        
        # The order of the standard wreath product A \wr B is |A|^|B| * |B|
        # The order of its Sylow p-subgroup is the p-part of |A \wr B|
        # We compute it as (p_part(|A|, p)^|B|) * p_part(|B|, p) to avoid huge integers
        sylow_AB_order = (p_part(A_order, p) ** B_order) * p_part(B_order, p)
        
        # If the orders are different, they cannot be isomorphic.
        # (Mathematically, if the orders are equal, then |Q| = |B|, meaning B is a p-group,
        # in which case P \wr B is indeed a Sylow p-subgroup of A \wr B and they are isomorphic.
        # Thus, checking order inequality is both necessary and sufficient for the conclusion to fail.)
        neg_q = bool(wreath_PQ_order != sylow_AB_order)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "H_2: p divides the order of A",
    "H_3: p divides the order of B",
    "H_4: P is a Sylow p-subgroup of A",
    "H_5: Q is a Sylow p-subgroup of B",
    "¬Q: P \\wr Q is not isomorphic to a Sylow p-subgroup of A \\wr B"
]

N_HYP = 5
NEG_Q_INDEX = 5