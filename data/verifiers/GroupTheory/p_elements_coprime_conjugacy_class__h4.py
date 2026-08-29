import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, p, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H_3: x is an element of G whose order is a power of p
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(x, Permutation):
            h3 = False
        elif not isinstance(p, (int, sympy.Integer)) or p < 2:
            h3 = False
        elif not G.contains(x):
            h3 = False
        else:
            order = x.order()
            if order == 1:
                h3 = True
            else:
                temp = order
                while temp % p == 0:
                    temp //= p
                h3 = (temp == 1)
    except Exception:
        h3 = False
        
    # neg_Q: For all Sylow p-subgroups P of G, x is not in the center of P
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(x, Permutation):
            neg_q = False
        elif not isinstance(p, (int, sympy.Integer)) or p < 2:
            neg_q = False
        else:
            P = G.sylow_subgroup(p)
            P_gens = P.generators
            
            def in_center_of_P(elem):
                if not P.contains(elem):
                    return False
                for gen in P_gens:
                    if elem * gen != gen * elem:
                        return False
                return True

            # Compute the conjugacy class of x in G
            orbit = {x}
            frontier = [x]
            gens = G.generators
            while frontier:
                curr = frontier.pop()
                for g in gens:
                    nxt = ~g * curr * g
                    if nxt not in orbit:
                        orbit.add(nxt)
                        frontier.append(nxt)
                        
            # Check if any conjugate of x is in the center of P
            exists_in_center = False
            for conj_x in orbit:
                if in_center_of_P(conj_x):
                    exists_in_center = True
                    break
                    
            neg_q = not exists_in_center
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: x is an element of G whose order is a power of p",
    "¬Q: For all Sylow p-subgroups P of G, x is not in the center of P"
]

N_HYP = 3
NEG_Q_INDEX = 3