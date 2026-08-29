import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math

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

def is_p_nilpotent(G, p):
    if not isinstance(p, int) or not sympy.isprime(p):
        return False
    if not isinstance(G, PermutationGroup):
        return False
    order = G.order()
    if order == 0:
        return False
    m = order
    while m % p == 0:
        m //= p
        
    p_prime_elements = []
    for g in G.generate_dimino():
        if math.gcd(g.order(), p) == 1:
            p_prime_elements.append(g)
            
    if len(p_prime_elements) != m:
        return False
        
    if not p_prime_elements:
        return False
        
    H_sub = PermutationGroup(p_prime_elements)
    return H_sub.order() == m

def direct_product(G, H):
    try:
        return G * H
    except Exception:
        pass
    
    gens = []
    degG = G.degree
    degH = H.degree
    if degG == 0:
        degG = 1
    if degH == 0:
        degH = 1
        
    for g in G.generators:
        a = list(g.array_form)
        if len(a) < degG:
            a += list(range(len(a), degG))
        a += list(range(degG, degG + degH))
        gens.append(Permutation(a))
        
    for h in H.generators:
        a = list(range(degG))
        b = list(h.array_form)
        if len(b) < degH:
            b += list(range(len(b), degH))
        a += [x + degG for x in b]
        gens.append(Permutation(a))
        
    if not gens:
        return PermutationGroup([Permutation(degG + degH - 1)])
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        p, G, H = witness
    except Exception:
        return [False] * 5

    # H_1: Let p be a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: Let G be a finite group
    try:
        h2 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h2 = False

    # H_3: Let H be a finite group
    try:
        h3 = isinstance(H, PermutationGroup) and H.order() > 0
    except Exception:
        h3 = False

    # H_4: Assume G is p-nilpotent
    try:
        h4 = is_p_nilpotent(G, p)
    except Exception:
        h4 = False

    # ¬Q: The direct product G \times H is NOT a p-nilpotent group
    try:
        G_times_H = direct_product(G, H)
        neg_q = not is_p_nilpotent(G_times_H, p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite group",
    "H_3: H is a finite group",
    "H_4: G is p-nilpotent",
    "¬Q: G x H is not p-nilpotent"
]

N_HYP = 4
NEG_Q_INDEX = 4