import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            P = witness['P']
            p = witness['p']
            degree_L_K = witness['degree_L_K']
        else:
            G, P, p, degree_L_K = witness
    except Exception:
        return [False, False, False]

    # H_1: G = Gal(L/K) is the Galois group of the extension
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(degree_L_K, (int, sympy.Integer)) and 
              degree_L_K > 0 and 
              degree_L_K % G.order() == 0)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isprime(p):
            h2 = False
        elif not isinstance(P, PermutationGroup):
            h2 = False
        else:
            is_subgroup = all(g in G for g in P.generators)
            order_P = P.order()
            order_G = G.order()
            
            is_power = False
            if order_P > 0:
                temp = order_P
                while temp % p == 0:
                    temp //= p
                if temp == 1:
                    is_power = True
                    
            is_sylow = is_power and (order_G // order_P) % p != 0
            h2 = is_subgroup and is_sylow
    except Exception:
        h2 = False

    # neg_Q: The degree of L^P over K is coprime to p, and the degree of L over L^P is a power of p.
    try:
        deg_L_LP = P.order()
        deg_LP_K = degree_L_K // deg_L_LP
        
        is_power = False
        if deg_L_LP > 0:
            temp = deg_L_LP
            while temp % p == 0:
                temp //= p
            if temp == 1:
                is_power = True
                
        coprime = (deg_LP_K % p != 0)
        
        neg_q = not (coprime and is_power)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is the Galois group of the extension",
    "H_2: P is a Sylow p-subgroup of G",
    "not Q: degree of L^P over K is not coprime to p, or degree of L over L^P is not a power of p"
]

N_HYP = 2
NEG_Q_INDEX = 2