import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
# We represent finite rings Z/nZ simply by the integer n >= 1.
Z = ZZ
Q = QQ
R = RR
C = CC

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def get_prime_ideals(n):
    """
    Returns a list of prime ideals of Z/nZ.
    Each prime ideal is represented as a set of integers.
    """
    if n == 1:
        return []
    prime_ideals = []
    for p in sympy.primefactors(n):
        ideal = set((k * p) % n for k in range(n))
        prime_ideals.append(ideal)
    return prime_ideals

def is_comm_ring_with_id(R_obj):
    """
    Checks if the given object represents a commutative ring with identity.
    """
    if isinstance(R_obj, int) and R_obj >= 1:
        return True
    if R_obj in (S.Integers, S.Rationals, S.Reals, S.Complexes, ZZ, QQ, RR, CC):
        return True
    if isinstance(R_obj, str) and R_obj in ("Z", "Q", "R", "C", "ZZ", "QQ", "RR", "CC"):
        return True
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (R1, R2, P), checks the remaining hypotheses and the negated conclusion.
    R1 and R2 are expected to be integers n >= 1 representing Z/nZ, or SymPy domains.
    P is expected to be an iterable of pairs (x, y) or a callable P(x, y).
    """
    try:
        R1, R2, P = witness
    except Exception:
        return [False, False]
        
    # H_1: R_1 and R_2 are commutative rings with identity
    try:
        h1 = is_comm_ring_with_id(R1) and is_comm_ring_with_id(R2)
    except Exception:
        h1 = False
        
    # ¬Q: P is NOT of the form P_1 x R_2 or R_1 x P_2 where P_1, P_2 are prime ideals
    try:
        if isinstance(R1, int) and isinstance(R2, int) and R1 >= 1 and R2 >= 1:
            if callable(P):
                P_set = set((x, y) for x in range(R1) for y in range(R2) if P(x, y))
            else:
                P_set = set()
                for item in P:
                    try:
                        P_set.add(tuple(item))
                    except TypeError:
                        P_set.add(item)
                        
            P1_list = get_prime_ideals(R1)
            P2_list = get_prime_ideals(R2)
            
            R1_set = set(range(R1))
            R2_set = set(range(R2))
            
            neg_q = True
            for p1 in P1_list:
                expected = set((x, y) for x in p1 for y in R2_set)
                if P_set == expected:
                    neg_q = False
                    break
                    
            if neg_q:
                for p2 in P2_list:
                    expected = set((x, y) for x in R1_set for y in p2)
                    if P_set == expected:
                        neg_q = False
                        break
        else:
            # For infinite rings, a finite set P cannot be P_1 x R_2 or R_1 x P_2
            # because prime ideals are non-empty (they contain 0), making the product infinite.
            if isinstance(P, (set, list, tuple)):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are commutative rings with identity",
    "¬Q: P is not of the form P_1 x R_2 or R_1 x P_2"
]

N_HYP = 1
NEG_Q_INDEX = 1