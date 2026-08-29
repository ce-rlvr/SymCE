import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
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

def is_sylow_p_subgroup(P, G, p):
    try:
        if p <= 1: 
            return False
        if not isinstance(P, PermutationGroup): 
            return False
        if not isinstance(G, PermutationGroup): 
            return False
        
        # Check if P is a subgroup of G
        for gen in P.generators:
            if gen not in G:
                return False
                
        order_G = G.order()
        order_P = P.order()
        
        # If P is trivial, it's a Sylow p-subgroup iff p does not divide |G|
        if order_P == 1:
            return order_G % p != 0
            
        # Check if |P| is a power of p
        k = 0
        temp = order_P
        while temp % p == 0:
            temp //= p
            k += 1
        if temp != 1: 
            return False
            
        # Check if it's the maximal power of p dividing |G|
        if order_G % (p**(k+1)) == 0: 
            return False
            
        return True
    except Exception:
        return False

def count_sylow(G, P):
    try:
        P_elems = frozenset(P.generate())
        orbit = set([P_elems])
        queue = [P_elems]
        G_gens = G.generators
        
        # BFS to find the number of conjugates of P in G
        while queue:
            curr = queue.pop(0)
            for g in G_gens:
                conj = frozenset([g * x * ~g for x in curr])
                if conj not in orbit:
                    orbit.add(conj)
                    queue.append(conj)
        return len(orbit)
    except Exception:
        return -1

def conclusion(G, p, P, H):
    if not is_sylow_p_subgroup(P, H, p):
        return False
    n_p_G = count_sylow(G, P)
    n_p_H = count_sylow(H, P)
    if n_p_G == -1 or n_p_H == -1:
        return False
    if n_p_H == 0:
        return False
    return n_p_G % n_p_H == 0

def conditions(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        p = witness.get('p')
        P = witness.get('P')
        H = witness.get('H')
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        G, p, P, H = witness
    else:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        h3 = bool(is_sylow_p_subgroup(P, G, p))
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails
    try:
        q = conclusion(G, p, P, H)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P is not a Sylow p-subgroup of H, or the number of Sylow p-subgroups of H does not divide the number of Sylow p-subgroups of G"
]

N_HYP = 3
NEG_Q_INDEX = 3