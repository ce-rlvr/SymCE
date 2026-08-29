import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

# Top-level setup
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
    try:
        G, p, n, m = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: The order of G is p^n * m
    try:
        h2 = (G.order() == (p**n) * m)
    except Exception:
        h2 = False
        
    # H_3: p is a prime number
    try:
        h3 = bool(isprime(p))
    except Exception:
        h3 = False
        
    # H_4: n is an integer greater than or equal to 1
    try:
        h4 = (int(n) == n) and (n >= 1)
    except Exception:
        h4 = False
        
    # ¬Q: G does not contain a Sylow p-subgroup of order p^n
    try:
        if not isprime(p):
            neg_q = False
        else:
            order = G.order()
            highest_power = 0
            temp = order
            p_int = int(p)
            while temp > 0 and temp % p_int == 0:
                highest_power += 1
                temp //= p_int
            
            # The conclusion states G contains a subgroup of order p^n known as a Sylow p-subgroup.
            # This means the Sylow p-subgroup has order p^n, which is true iff highest_power == n.
            conclusion = (highest_power == n)
            neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^n * m",
    "H_3: p is a prime number",
    "H_4: n is an integer greater than or equal to 1",
    "¬Q: G does not contain a Sylow p-subgroup of order p^n"
]

N_HYP = 4
NEG_Q_INDEX = 4