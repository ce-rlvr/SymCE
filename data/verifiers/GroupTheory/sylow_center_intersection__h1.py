import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Given a witness (G, P, p), checks if it is a valid counterexample.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not isinstance(G, PermutationGroup):
            h2 = False
        elif p <= 1:
            h2 = False
        else:
            # Check if P is a subgroup of G
            is_sub = all(G.contains(g) for g in P.generators)
            
            # Check if P is a p-group
            order_P = P.order()
            temp = order_P
            while temp % p == 0 and temp > 1:
                temp //= p
            is_p_group = (temp == 1)
            
            # Check if P is maximal (order is the highest power of p dividing |G|)
            order_G = G.order()
            max_p = 1
            while order_G % p == 0:
                max_p *= p
                order_G //= p
                
            h2 = bool(is_sub and is_p_group and order_P == max_p)
    except Exception:
        h2 = False

    # neg_Q: P \cap Z(G) is NOT the unique Sylow p-subgroup of Z(G)
    try:
        if not isinstance(P, PermutationGroup) or not isinstance(G, PermutationGroup):
            neg_q = False
        elif p <= 1:
            neg_q = False
        else:
            Z = G.center()
            
            # Compute the order of the intersection P \cap Z(G)
            if P.order() < Z.order():
                order_I = sum(1 for g in P.generate() if Z.contains(g))
            else:
                order_I = sum(1 for g in Z.generate() if P.contains(g))
                
            # Find the highest power of p dividing |Z(G)|
            order_Z = Z.order()
            max_p_Z = 1
            while order_Z % p == 0:
                max_p_Z *= p
                order_Z //= p
                
            # Since Z(G) is abelian, its Sylow p-subgroup is unique if it exists.
            # We just need to check if the intersection has the correct maximal order.
            is_sylow_of_Z = (order_I == max_p_Z)
            
            neg_q = not is_sylow_of_Z
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap Z(G) is not the unique Sylow p-subgroup of Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2