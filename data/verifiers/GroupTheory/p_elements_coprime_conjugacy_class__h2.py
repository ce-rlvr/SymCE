import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import isprime

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G whose order is a power of p",
    "H_3: The size of the conjugacy class of x in G is coprime to p",
    "¬Q: There does not exist a Sylow p-subgroup P of G such that x is in the center of P"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_power_of(n, p):
    if n == 1:
        return True
    if p == 0 or p == 1:
        return False
    if p < 0:
        return False
    while n % p == 0:
        n //= p
    return n == 1

def conditions(witness):
    try:
        G, x, p = witness
        if not float(p).is_integer():
            return [False, False, False, False]
        p = int(p)
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: x is an element of G whose order is a power of p
    try:
        if x in G:
            order = x.order()
            h2 = is_power_of(order, p)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: The size of the conjugacy class of x in G is coprime to p
    try:
        try:
            C = G.centralizer(x)
            class_size = G.order() // C.order()
        except Exception:
            try:
                C = G.centralizer(PermutationGroup([x]))
                class_size = G.order() // C.order()
            except Exception:
                conj_class = {x}
                queue = [x]
                gens = G.generators
                gens_and_inv = list(gens) + [~g for g in gens]
                while queue:
                    curr = queue.pop(0)
                    for g in gens_and_inv:
                        nxt = g * curr * ~g
                        if nxt not in conj_class:
                            conj_class.add(nxt)
                            queue.append(nxt)
                class_size = len(conj_class)
        h3 = math.gcd(class_size, p) == 1
    except Exception:
        h3 = False
        
    # neg_Q: There does not exist a Sylow p-subgroup P of G such that x is in the center of P
    try:
        if not isprime(p):
            # Sylow p-subgroups are only defined for primes.
            # If p is not prime, no such subgroup exists, making the existence statement false.
            neg_q = True
        else:
            try:
                P0 = G.sylow_subgroup(p)
                try:
                    Z_P0 = P0.center()
                    check_in_Z = lambda c: c in Z_P0
                except Exception:
                    P0_gens = P0.generators
                    P0_elems = list(P0.elements)
                    Z_P0_elems = [y for y in P0_elems if all(y*g == g*y for g in P0_gens)]
                    check_in_Z = lambda c: c in Z_P0_elems
                
                conj_class = {x}
                queue = [x]
                gens = G.generators
                gens_and_inv = list(gens) + [~g for g in gens]
                while queue:
                    curr = queue.pop(0)
                    for g in gens_and_inv:
                        nxt = g * curr * ~g
                        if nxt not in conj_class:
                            conj_class.add(nxt)
                            queue.append(nxt)
                
                exists = any(check_in_Z(c) for c in conj_class)
                neg_q = not exists
            except Exception:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]