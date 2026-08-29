import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_nilpotency_class(G):
    if hasattr(G, 'nilpotency_class'):
        try:
            return G.nilpotency_class
        except Exception:
            pass
            
    if G.order() == 1:
        return 0
    if not getattr(G, 'is_nilpotent', True):
        return float('inf')
        
    elements = list(G.elements)
    id_elem = next(g for g in elements if g.is_Identity)
    
    L = G
    c = 0
    while L.order() > 1:
        gens = []
        for h in L.generators:
            for g in G.generators:
                comm = (h**-1) * (g**-1) * h * g
                if comm != id_elem:
                    gens.append(comm)
        closure = set(gens)
        queue = list(gens)
        while queue:
            x = queue.pop(0)
            for g in G.generators:
                cx = (g**-1) * x * g
                if cx not in closure:
                    closure.add(cx)
                    queue.append(cx)
        if not closure:
            L = PermutationGroup([id_elem])
        else:
            L = PermutationGroup(list(closure))
        c += 1
        if c > 20:
            return float('inf')
    return c

def conditions(witness) -> list[bool]:
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H2: The nilpotency class of G is strictly less than p
    try:
        p_int = int(p)
        c = get_nilpotency_class(G)
        h2 = bool(c < p_int)
    except Exception:
        h2 = False
        
    # neg_Q: G is NOT a regular p-group
    try:
        p_int = int(p)
        order = G.order()
        is_p_group = True
        
        if p_int <= 1:
            is_p_group = False
        elif order == 1:
            is_p_group = True
        else:
            temp = order
            while temp % p_int == 0:
                temp //= p_int
            if temp != 1:
                is_p_group = False
                
        if not is_p_group:
            is_regular = False
        else:
            is_regular = True
            elements = list(G.elements)
            id_elem = next(g for g in elements if g.is_Identity)
            
            G_prime = G.derived_subgroup()
            G_mho_gens = [k ** p_int for k in G_prime.elements if k ** p_int != id_elem]
            if not G_mho_gens:
                G_mho_1_elements = {id_elem}
            else:
                G_mho_1 = PermutationGroup(G_mho_gens)
                G_mho_1_elements = set(G_mho_1.elements)
                
            for x in elements:
                for y in elements:
                    xy = x * y
                    xy_p = xy ** p_int
                    x_p = x ** p_int
                    y_p = y ** p_int
                    target = (x_p * y_p)**-1 * xy_p
                    
                    if target == id_elem:
                        continue
                        
                    if target not in G_mho_1_elements:
                        is_regular = False
                        break
                    
                    gens = [g for g in (x, y) if g != id_elem]
                    if not gens:
                        H = PermutationGroup([id_elem])
                    else:
                        H = PermutationGroup(gens)
                    
                    H_prime = H.derived_subgroup()
                    mho_gens = [k ** p_int for k in H_prime.elements if k ** p_int != id_elem]
                    if not mho_gens:
                        mho_1_elements = {id_elem}
                    else:
                        mho_1 = PermutationGroup(mho_gens)
                        mho_1_elements = set(mho_1.elements)
                        
                    if target not in mho_1_elements:
                        is_regular = False
                        break
                if not is_regular:
                    break
                    
        neg_q = not is_regular
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The nilpotency class of G is strictly less than p",
    "¬Q: G is not a regular p-group"
]

N_HYP = 2
NEG_Q_INDEX = 2