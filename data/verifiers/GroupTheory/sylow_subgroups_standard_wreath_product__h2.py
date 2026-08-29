import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def p_part(n, p):
    """Returns the highest power of prime p dividing n."""
    if p <= 1 or n <= 0:
        return 0
    ans = 1
    while n % p == 0:
        ans *= p
        n //= p
    return ans

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 5:
            return [False] * 5
        A, B, P, Q, p = witness
    except Exception:
        return [False] * 5
    
    # H_1: A and B are finite groups
    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of A
    try:
        if isinstance(P, PermutationGroup) and isinstance(A, PermutationGroup):
            is_sub = all(g in A for g in P.generators)
            is_sylow = P.order() == p_part(A.order(), p)
            h3 = is_sub and is_sylow
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # H_4: Q is a Sylow p-subgroup of B
    try:
        if isinstance(Q, PermutationGroup) and isinstance(B, PermutationGroup):
            is_sub = all(g in B for g in Q.generators)
            is_sylow = Q.order() == p_part(B.order(), p)
            h4 = is_sub and is_sylow
        else:
            h4 = False
    except Exception:
        h4 = False
        
    # ¬Q: P \wr Q is not isomorphic to a Sylow p-subgroup of A \wr B
    # Two finite p-groups are isomorphic only if they have the same order.
    # We check if the order of P \wr Q differs from the order of a Sylow p-subgroup of A \wr B.
    try:
        if isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and \
           isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup):
            p_val = int(p)
            if p_val > 1:
                # Order of A \wr B is |A|^|B| * |B|
                # Highest power of p dividing it is p_part(|A|, p)^|B| * p_part(|B|, p)
                sylow_order_A_wr_B = (p_part(A.order(), p_val) ** B.order()) * p_part(B.order(), p_val)
                
                # Order of P \wr Q is |P|^|Q| * |Q|
                order_P_wr_Q = (P.order() ** Q.order()) * Q.order()
                
                neg_q = order_P_wr_Q != sylow_order_A_wr_B
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are finite groups",
    "H_2: p is a prime",
    "H_3: P is a Sylow p-subgroup of A",
    "H_4: Q is a Sylow p-subgroup of B",
    "¬Q: P \\wr Q is not isomorphic to a Sylow p-subgroup of A \\wr B"
]

N_HYP = 4
NEG_Q_INDEX = 4