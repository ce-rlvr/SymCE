import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import math

# Top-level setup: named object bindings that the witness expression may reference
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

def conditions(witness) -> list[bool]:
    try:
        p, G, P = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    # H_2: G is the symmetric group S_p on p letters
    try:
        h2_ok = (
            isinstance(G, sympy.combinatorics.PermutationGroup) and 
            G.degree == p and 
            G.order() == math.factorial(p)
        )
    except Exception:
        h2_ok = False

    # ¬Q: The order of the normalizer N_G(P) is NOT exactly p(p-1)
    try:
        deg = G.degree
        # Ensure all elements of P are padded to the degree of G for safe multiplication and comparison
        P_gens = [Permutation(x, size=deg) for x in P.generators]
        P_elements = set(Permutation(x, size=deg) for x in P.generate())
        
        norm_order = 0
        for i, g in enumerate(G.generate()):
            if i > 100000:
                # Safeguard against excessively large groups timing out the verifier
                raise ValueError("Group too large to verify by brute force")
            
            # Check if g normalizes P: g * x * g^-1 in P for all generators x of P
            # In SymPy, ~g is the inverse of g, and permutations are applied left-to-right.
            if all((g * x * ~g) in P_elements for x in P_gens):
                norm_order += 1
                
        neg_q_ok = norm_order != p * (p - 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is the symmetric group S_p on p letters",
    "¬Q: The order of the normalizer N_G(P) is not exactly p(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2