import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = AbelianGroup(2, 2)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Extract or infer G, p, q from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            n = G.order()
            p, q = 1, n
            for i in range(1, int(math.isqrt(n)) + 1):
                if n % i == 0:
                    p_cand = i
                    q_cand = n // i
                    if p_cand < q_cand and (q_cand - 1) % p_cand != 0:
                        p, q = p_cand, q_cand
                        break
    except Exception:
        return [False] * 5

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: The order of G is p * q
    try:
        h2 = bool(G.order() == p * q)
    except Exception:
        h2 = False

    # H3: p is strictly less than q
    try:
        h3 = bool(p < q)
    except Exception:
        h3 = False

    # H4: p does not divide q - 1
    try:
        h4 = bool((q - 1) % p != 0)
    except Exception:
        h4 = False

    # ¬Q: Conclusion fails
    # The conclusion states G has unique normal Sylow p- and q-subgroups, and is cyclic of order pq.
    # If p or q is not prime, the concept of a Sylow p-subgroup is undefined/invalid, making the conclusion false.
    # If G is not cyclic, the conclusion is also false.
    try:
        is_cyclic = False
        if hasattr(G, 'generators') and len(G.generators) == 1:
            is_cyclic = True
        elif G.order() <= 5000:
            for g in G.elements:
                if g.order() == p * q:
                    is_cyclic = True
                    break
        
        conclusion_holds = isprime(p) and isprime(q) and is_cyclic
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p * q",
    "H_3: p is strictly less than q",
    "H_4: p does not divide q - 1",
    "¬Q: G does not have unique normal Sylow p- and q-subgroups, or is not isomorphic to the cyclic group of order pq"
]

N_HYP = 4
NEG_Q_INDEX = 4