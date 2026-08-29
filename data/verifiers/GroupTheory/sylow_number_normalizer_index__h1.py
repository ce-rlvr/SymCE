import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            G = witness[0]
            p = witness[1]
            P = witness[2]
        else:
            G = witness.G
            p = witness.p
            P = witness.P
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime dividing the order of G
    try:
        h1 = sympy.isprime(p) and (G.order() % p == 0)
    except Exception:
        h1 = False
        
    # H2: P is a Sylow p-subgroup of G
    try:
        order_G = G.order()
        order_P = P.order()
        
        temp = order_P
        while temp % p == 0 and temp > 1:
            temp //= p
            
        if temp == 1 and (order_G // order_P) % p != 0:
            if hasattr(P, 'generators'):
                is_sub = all(gen in G for gen in P.generators)
            elif hasattr(P, 'is_subgroup'):
                is_sub = P.is_subgroup(G)
            else:
                is_sub = True
            h2 = is_sub
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The number of Sylow p-subgroups of G is not equal to the index of N_G(P) in G
    try:
        neg_q = False
        if isinstance(witness, (tuple, list)) and len(witness) >= 5:
            n_p = witness[3]
            index = witness[4]
            neg_q = (n_p != index)
        else:
            n_p = None
            index = None
            
            if hasattr(G, 'n_p'):
                n_p = G.n_p(p)
            elif hasattr(G, 'sylow_p_subgroups'):
                n_p = len(G.sylow_p_subgroups(p))
                
            if hasattr(G, 'normalizer_index'):
                index = G.normalizer_index(P)
            elif hasattr(G, 'normalizer'):
                N = G.normalizer(P)
                index = G.order() // N.order()
                
            if n_p is not None and index is not None:
                neg_q = (n_p != index)
            elif hasattr(G, 'generate') and hasattr(P, 'generate'):
                P_elements = set(P.generate())
                conjugates = []
                n_order = 0
                for g in G.generate():
                    conj = frozenset({g * x * ~g for x in P_elements})
                    if conj not in conjugates:
                        conjugates.append(conj)
                    if conj == frozenset(P_elements):
                        n_order += 1
                n_p_manual = len(conjugates)
                index_manual = G.order() // n_order
                neg_q = (n_p_manual != index_manual)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The number of Sylow p-subgroups of G is not equal to the index (G : N_G(P))"
]

N_HYP = 2
NEG_Q_INDEX = 2