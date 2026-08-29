import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
    "H_2: P is a Sylow p-subgroup of \\Phi(G)",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def frattini_subgroup(G):
    """Computes the Frattini subgroup of a finite permutation group G."""
    subgroups = G.subgroups()
    order_G = G.order()
    proper = [H for H in subgroups if H.order() < order_G]
    if not proper:
        return G
    
    maximal = []
    for H in proper:
        is_max = True
        for K in proper:
            if H.order() < K.order() and all(g in K for g in H.generators):
                is_max = False
                break
        if is_max:
            maximal.append(H)
            
    if not maximal:
        return G
        
    F_elements = set(maximal[0].generate())
    for M in maximal[1:]:
        F_elements = F_elements.intersection(set(M.generate()))
        
    return PermutationGroup(list(F_elements))

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, P, p_val = witness
            elif len(witness) == 2:
                G, P = witness
                p_val = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: P is a Sylow p-subgroup of \Phi(G)
    try:
        h2 = False
        if h1 and isinstance(P, PermutationGroup):
            F = frattini_subgroup(G)
            # Check if P is a subgroup of F
            if all(g in F for g in P.generators):
                order_P = P.order()
                order_F = F.order()
                factors = factorint(order_P)
                
                if p_val is not None:
                    if order_P > 1:
                        if len(factors) == 1 and list(factors.keys())[0] == p_val:
                            if (order_F // order_P) % p_val != 0:
                                h2 = True
                    else:
                        if (order_F // order_P) % p_val != 0:
                            h2 = True
                else:
                    if len(factors) == 0:
                        h2 = True
                    elif len(factors) == 1:
                        p = list(factors.keys())[0]
                        if (order_F // order_P) % p != 0:
                            h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: P is NOT a normal subgroup of G
    try:
        neg_q = False
        if h1 and isinstance(P, PermutationGroup):
            # First ensure P is a subgroup of G
            if all(g in G for g in P.generators):
                is_normal = True
                for g in G.generate():
                    for p in P.generators:
                        conj = g * p * (g**-1)
                        if conj not in P:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]