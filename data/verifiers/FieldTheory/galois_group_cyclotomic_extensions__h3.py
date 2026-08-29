import math
from sympy.ntheory import factorint, isprime
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, PermutationGroup
)

# Top-level setup: named object bindings that the witness expression may reference
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

def get_ZnZ_star_invariants(n):
    if n <= 0: 
        return {}
    factors = factorint(n)
    invs = []
    for p, k in factors.items():
        if p == 2:
            if k == 1:
                pass
            elif k == 2:
                invs.append(2)
            else:
                invs.append(2)
                invs.append(2**(k-2))
        else:
            order = (p**(k-1)) * (p - 1)
            invs.append(order)
            
    sylows = {}
    for order in invs:
        for q, e in factorint(order).items():
            sylows.setdefault(q, []).append(e)
    for q in sylows:
        sylows[q].sort(reverse=True)
    return sylows

def get_G_invariants(G):
    try:
        order_G = G.order()
    except TypeError:
        order_G = G.order
        
    if order_G == 1:
        return {}
        
    if order_G > 2000:
        raise ValueError("Group too large for fast verification")
        
    try:
        elements = list(G.generate())
    except Exception:
        elements = list(G.elements)
        
    q_sylows = {}
    for q in factorint(order_G).keys():
        sylow_q_orders = []
        for g in elements:
            try:
                o = g.order()
            except TypeError:
                o = g.order
            if o == 1 or set(factorint(o).keys()) == {q}:
                sylow_q_orders.append(o)
                
        k = 1
        a_i_ge_k = []
        while True:
            count_div_qk = sum(1 for o in sylow_q_orders if o <= q**k)
            
            temp = count_div_qk
            fk = 0
            while temp > 1:
                temp //= q
                fk += 1
                
            count_div_qk_minus_1 = sum(1 for o in sylow_q_orders if o <= q**(k-1))
            temp = count_div_qk_minus_1
            fk_minus_1 = 0
            while temp > 1:
                temp //= q
                fk_minus_1 += 1
                
            num_invariants_ge_k = fk - fk_minus_1
            if num_invariants_ge_k == 0:
                break
            a_i_ge_k.append(num_invariants_ge_k)
            k += 1
            
        invariants = []
        if a_i_ge_k:
            for i in range(a_i_ge_k[0]):
                val = sum(1 for count in a_i_ge_k if count > i)
                invariants.append(val)
                
        q_sylows[q] = sorted(invariants, reverse=True)
        
    return q_sylows

def is_subgroup_of_ZnZ_star(G, n):
    if not G.is_abelian:
        return False
    
    H_sylows = get_ZnZ_star_invariants(n)
    G_sylows = get_G_invariants(G)
    
    for q, g_invs in G_sylows.items():
        if q not in H_sylows:
            return False
        h_invs = H_sylows[q]
        if len(g_invs) > len(h_invs):
            return False
        for a, b in zip(g_invs, h_invs):
            if a > b:
                return False
    return True

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (char_F, n, G) or (n, G)
    where char_F is the characteristic of the field F (0 or prime),
    n is the integer, and G is the Galois group Gal(E/F) as a PermutationGroup.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                char_F, n, G = witness
            elif len(witness) == 2:
                n, G = witness
                char_F = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: F is a field (its characteristic is 0 or a prime number)
    try:
        h1 = (int(char_F) == 0) or isprime(int(char_F))
    except Exception:
        h1 = False
        
    # H2: n is a positive integer such that the characteristic of F does not divide n
    try:
        n_val = int(n)
        char_F_val = int(char_F)
        h2 = (n_val > 0) and (char_F_val == 0 or n_val % char_F_val != 0)
    except Exception:
        h2 = False
        
    # neg_Q: The Galois group Gal(E/F) is NOT isomorphic to a subgroup of (Z/nZ)^x
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            neg_q = not is_subgroup_of_ZnZ_star(G, n_val)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer such that the characteristic of F does not divide n",
    "¬Q: The Galois group Gal(E/F) is not isomorphic to a subgroup of the multiplicative group (Z/nZ)^x"
]

N_HYP = 2
NEG_Q_INDEX = 2