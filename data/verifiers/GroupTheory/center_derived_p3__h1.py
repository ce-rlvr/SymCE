import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime, factorint

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

def conditions(witness) -> list[bool]:
    # Extract p and G from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, G = witness
        else:
            G = witness
            order = G.order()
            factors = factorint(order)
            # If the order is a power of a single prime, infer p
            if len(factors) == 1:
                p = list(factors.keys())[0]
            else:
                p = 0
    except Exception:
        p = 0
        G = None

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H_2: The order of G is p^3
    try:
        h2_ok = bool(G.order() == p**3)
    except Exception:
        h2_ok = False

    # ¬Q: The center Z(G) is NOT equal to the derived subgroup G'
    try:
        Z = G.center()
        D = G.derived_subgroup()
        
        # Check if Z is a subgroup of D and D is a subgroup of Z
        z_in_d = all(D.contains(g) for g in Z.generators)
        d_in_z = all(Z.contains(g) for g in D.generators)
        
        neg_q_ok = not (z_in_d and d_in_z)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is p^3",
    "¬Q: The center Z(G) is not equal to the derived subgroup G'"
]

N_HYP = 2
NEG_Q_INDEX = 2