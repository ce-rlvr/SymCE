import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_degree(G):
    return G.degree if G.degree > 0 else 1

def p_power(n, p):
    ans = 1
    while n > 0 and n % p == 0:
        ans *= p
        n //= p
    return ans

def wreath_product(A, B):
    n = get_degree(A)
    m = get_degree(B)
    
    gens = []
    
    for gen_b in B.generators:
        if gen_b.is_Identity: 
            continue
        p = list(range(n * m))
        for y in range(m):
            new_y = gen_b(y) if y < gen_b.size else y
            for x in range(n):
                p[y * n + x] = new_y * n + x
        gens.append(Permutation(p))
        
    for gen_a in A.generators:
        if gen_a.is_Identity: 
            continue
        for c in range(m):
            p = list(range(n * m))
            for x in range(n):
                new_x = gen_a(x) if x < gen_a.size else x
                p[c * n + x] = c * n + new_x
            gens.append(Permutation(p))
            
    if not gens:
        return PermutationGroup([Permutation(n * m - 1)])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            p = witness.get('p')
            P = witness.get('P')
            Q = witness.get('Q')
        else:
            A, B, p, P, Q = witness
    except Exception:
        return [False, False, False]
        
    # H1: A and B are finite groups
    try:
        h1 = bool(isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and
                  isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup))
    except Exception:
        h1 = False
        
    # H2: p is a prime dividing the orders of A and B
    try:
        h2 = bool(isprime(p) and (A.order() % p == 0) and (B.order() % p == 0))
    except Exception:
        h2 = False
        
    # neg_Q: P \wr Q is NOT isomorphic to a Sylow p-subgroup of A \wr B
    try:
        deg_B = get_degree(B)
        order_A_wr_B = (A.order() ** deg_B) * B.order()
        sylow_order = p_power(order_A_wr_B, p)
        
        deg_Q = get_degree(Q)
        order_P_wr_Q = (P.order() ** deg_Q) * Q.order()
        
        if order_P_wr_Q != sylow_order:
            neg_q = True
        else:
            if get_degree(A) * get_degree(B) > 200:
                # Prevent timeout for excessively large groups if orders happen to match
                neg_q = False
            else:
                A_wr_B = wreath_product(A, B)
                Sylow = A_wr_B.sylow_subgroup(p)
                P_wr_Q = wreath_product(P, Q)
                neg_q = not P_wr_Q.is_isomorphic(Sylow)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are finite groups",
    "H_2: p is a prime dividing the orders of A and B",
    "¬Q: P \\wr Q is not isomorphic to a Sylow p-subgroup of A \\wr B"
]

N_HYP = 2
NEG_Q_INDEX = 2