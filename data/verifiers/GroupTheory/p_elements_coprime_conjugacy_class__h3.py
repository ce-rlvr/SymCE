import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
        G, p, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H3: The size of the conjugacy class of x in G is coprime to p
    orbit = set()
    try:
        if not isinstance(x, Permutation):
            h3 = False
        elif x not in G:
            h3 = False
        else:
            orbit = {x}
            frontier = [x]
            gens = G.generators
            while frontier:
                curr = frontier.pop()
                for g in gens:
                    c1 = g * curr * (~g)
                    if c1 not in orbit:
                        orbit.add(c1)
                        frontier.append(c1)
                    c2 = (~g) * curr * g
                    if c2 not in orbit:
                        orbit.add(c2)
                        frontier.append(c2)
            h3 = (math.gcd(len(orbit), p) == 1)
    except Exception:
        h3 = False
        
    # neg_Q: For all Sylow p-subgroups P of G, x is not in the center of P
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            P0 = G.sylow_subgroup(p)
            P0_gens = P0.generators
            Z_P0 = set()
            for elem in P0.generate():
                if all(elem * g == g * elem for g in P0_gens):
                    Z_P0.add(elem)
            
            intersect = False
            for c in orbit:
                if c in Z_P0:
                    intersect = True
                    break
            neg_q = not intersect
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: The size of the conjugacy class of x in G is coprime to p",
    "¬Q: For all Sylow p-subgroups P of G, x is not in the center of P"
]

N_HYP = 3
NEG_Q_INDEX = 3