import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import isprime
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: p^2 does not divide the order of G",
    "H_4: P and Q are distinct Sylow p-subgroups of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {e}"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        G, p, P, Q = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: p^2 does not divide the order of G
    try:
        h3 = (G.order() % (p**2)) != 0
    except Exception:
        h3 = False

    # H_4: P and Q are distinct Sylow p-subgroups of G
    try:
        def is_sylow_p(H, G_group, prime_p):
            if not isinstance(H, PermutationGroup):
                return False
            # Check if H is a subgroup of G
            for gen in H.generators:
                if gen not in G_group:
                    return False
            
            # Find the highest power of p dividing |G|
            order_G = G_group.order()
            k = 0
            while order_G % prime_p == 0:
                k += 1
                order_G //= prime_p
                
            return H.order() == (prime_p ** k)

        is_P_sylow = is_sylow_p(P, G, p)
        is_Q_sylow = is_sylow_p(Q, G, p)
        
        distinct = False
        if is_P_sylow and is_Q_sylow:
            # Since P and Q have the same finite order, they are distinct 
            # if and only if P is not a subgroup of Q.
            for gen in P.generators:
                if gen not in Q:
                    distinct = True
                    break
        
        h4 = is_P_sylow and is_Q_sylow and distinct
    except Exception:
        h4 = False

    # ¬Q: The intersection P \cap Q is not the trivial subgroup {e}
    try:
        try:
            elements_P = set(P.elements)
        except Exception:
            elements_P = set(P.generate())
            
        try:
            elements_Q = set(Q.elements)
        except Exception:
            elements_Q = set(Q.generate())
            
        intersection = elements_P.intersection(elements_Q)
        # The trivial subgroup contains exactly 1 element (the identity)
        neg_q = len(intersection) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]