import math
import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, p, P) or a dict with these keys, where:
      - G is the finite group
      - p is the prime number
      - P is a subgroup of G
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
        else:
            G, p, P = witness
            # Auto-correct if the user swapped p and P
            if isinstance(p, PermutationGroup) and isinstance(P, (int, sympy.Integer)):
                p, P = P, p
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(sympy.isprime(p))
    except Exception:
        h2 = False

    # ¬Q: The order of the quotient group N_G(P) / P is NOT coprime to p
    try:
        if not isinstance(P, PermutationGroup):
            neg_q = False
        elif not all(G.contains(x) for x in P.generators):
            neg_q = False
        elif G.order() > 5000:
            # Prevent timeouts for excessively large groups
            neg_q = False
        else:
            # Compute the order of the normalizer N_G(P)
            norm_order = 0
            for g in G.elements:
                is_in_norm = True
                for x in P.generators:
                    # Check if g * x * g^-1 is in P
                    if not P.contains(g * x * ~g):
                        is_in_norm = False
                        break
                if is_in_norm:
                    norm_order += 1
            
            p_order = P.order()
            if norm_order % p_order != 0:
                neg_q = False
            else:
                quotient_order = int(norm_order // p_order)
                p_int = int(p)
                # The conclusion fails if the quotient order is NOT coprime to p
                neg_q = math.gcd(quotient_order, p_int) != 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: The order of the quotient group N_G(P) / P is not coprime to p"
]

N_HYP = 2
NEG_Q_INDEX = 2