import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import isprime

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
    # Unpack witness. It can be a tuple (G, p) or just G (with p defaulting to 2)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = 2
    except Exception:
        G = witness
        p = 2

    # H_1: G is a non-abelian group
    try:
        h1_ok = bool(hasattr(G, 'is_abelian') and hasattr(G, 'center') and not G.is_abelian)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = bool(isprime(p))
    except Exception:
        h2_ok = False

    # ¬Q: The center Z(G) is NOT equal to the derived subgroup G'
    try:
        Z = G.center()
        D = G.derived_subgroup()
        
        is_equal = True
        for g in Z.generators:
            if g not in D:
                is_equal = False
                break
        if is_equal:
            for g in D.generators:
                if g not in Z:
                    is_equal = False
                    break
                    
        neg_q_ok = not is_equal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "H_2: p is a prime number",
    "¬Q: Z(G) != G'"
]

N_HYP = 2
NEG_Q_INDEX = 2