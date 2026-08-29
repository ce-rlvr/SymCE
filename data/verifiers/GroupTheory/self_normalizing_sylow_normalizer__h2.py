import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, P = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() <= 2048
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if h1 and isinstance(P, PermutationGroup):
            if P.is_subgroup(G):
                order_P = P.order()
                order_G = G.order()
                factors = factorint(order_P)
                if len(factors) == 0:
                    h2 = True
                elif len(factors) == 1:
                    p = list(factors.keys())[0]
                    if order_G % (order_P * p) != 0:
                        h2 = True
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if h1 and h2:
            G_elements = list(G.generate())
            P_elements = set(P.generate())
            P_gens = P.generators
            
            N_P_elements = []
            for g in G_elements:
                g_inv = ~g
                is_in_norm = True
                for h in P_gens:
                    if (g * h * g_inv) not in P_elements:
                        is_in_norm = False
                        break
                if is_in_norm:
                    N_P_elements.append(g)
                    
            N_P_set = set(N_P_elements)
            
            N_N_P_elements = []
            for g in G_elements:
                g_inv = ~g
                is_in_norm = True
                for h in N_P_elements:
                    if (g * h * g_inv) not in N_P_set:
                        is_in_norm = False
                        break
                if is_in_norm:
                    N_N_P_elements.append(g)
                    
            if len(N_N_P_elements) != len(N_P_elements):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: N_G(N_G(P)) != N_G(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2