import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z5 = CyclicGroup(5)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_cyclic(G):
    """Helper function to determine if a permutation group is cyclic."""
    try:
        if G.order() == 1:
            return True
        # A non-abelian group cannot be cyclic
        if not G.is_abelian:
            return False
        o = G.order()
        # Check if there is an element of order equal to the group's order
        for g in G.elements:
            if g.order() == o:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # Unpack witness. Accept either (G1, G2) or (G1, m, G2, n)
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G1, G2 = witness
            elif len(witness) == 4:
                G1, _, G2, _ = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: G_2 is a cyclic group of order n
    try:
        h1_ok = is_cyclic(G2)
    except Exception:
        h1_ok = False

    # ¬Q: The direct product group G_1 \times G_2 is cyclic if and only if gcd(m, n) = 1
    try:
        m = int(G1.order())
        n = int(G2.order())
        
        # A direct product of finite groups is cyclic iff both are cyclic and their orders are coprime.
        prod_is_cyclic = is_cyclic(G1) and is_cyclic(G2) and math.gcd(m, n) == 1
        
        # The conclusion is the biconditional statement
        q = (prod_is_cyclic == (math.gcd(m, n) == 1))
        
        # We want the conclusion to FAIL at the witness
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G_2 is a cyclic group of order n",
    "¬Q: The biconditional (G_1 x G_2 is cyclic iff gcd(m, n) = 1) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1