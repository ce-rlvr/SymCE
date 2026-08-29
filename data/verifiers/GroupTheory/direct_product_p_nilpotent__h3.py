import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
        p, G, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: Let p be a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: Let G and H be finite groups
    try:
        h2 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h2 = False
        
    def p_prime_part(n, p):
        n = int(n)
        p = int(p)
        if n <= 0: return 0
        while n % p == 0:
            n //= p
        return n
        
    def count_p_prime_elements(grp, p):
        count = 0
        p_int = int(p)
        for g in grp.elements:
            if math.gcd(int(g.order()), p_int) == 1:
                count += 1
        return count

    # H_3: Assume H is p-nilpotent
    # A finite group is p-nilpotent iff the number of elements of order coprime to p 
    # is exactly the p'-part of the group's order.
    try:
        if h1 and h2:
            h_p_prime = p_prime_part(H.order(), p)
            h_count = count_p_prime_elements(H, p)
            h3 = (h_count == h_p_prime)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The direct product G \times H is NOT a p-nilpotent group
    # The number of p'-elements in G x H is the product of the number of p'-elements in G and H.
    try:
        if h1 and h2:
            g_p_prime = p_prime_part(G.order(), p)
            g_count = count_p_prime_elements(G, p)
            
            h_p_prime = p_prime_part(H.order(), p)
            h_count = count_p_prime_elements(H, p)
            
            gh_p_prime = g_p_prime * h_p_prime
            gh_count = g_count * h_count
            
            neg_q = (gh_count != gh_p_prime)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G and H are finite groups",
    "H_3: H is p-nilpotent",
    "¬Q: G x H is not p-nilpotent"
]

N_HYP = 3
NEG_Q_INDEX = 3