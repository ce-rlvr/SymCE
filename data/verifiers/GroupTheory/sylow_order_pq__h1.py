import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint

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

def get_order(obj):
    o = obj.order
    return o() if callable(o) else o

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            order = get_order(G)
            factors = factorint(order)
            if len(factors) == 2 and all(v == 1 for v in factors.values()):
                p, q = sorted(factors.keys())
            elif len(factors) == 1 and list(factors.values())[0] == 2:
                p = q = list(factors.keys())[0]
            else:
                p, q = 0, 0
    except Exception:
        G, p, q = None, 0, 0

    try:
        h1 = (get_order(G) == p * q)
    except Exception:
        h1 = False

    try:
        h2 = isprime(p) and isprime(q)
    except Exception:
        h2 = False

    try:
        h3 = (p < q)
    except Exception:
        h3 = False

    try:
        h4 = ((q - 1) % p != 0)
    except Exception:
        h4 = False

    try:
        if not hasattr(G, 'order'):
            raise ValueError
        
        order = get_order(G)
        if p == 0 or q == 0 or order % p != 0 or order % q != 0:
            q_holds = False
        else:
            Sp = G.sylow_subgroup(p)
            unique_p = True
            for g in G.generators:
                ginv = ~g
                for h in Sp.generators:
                    if not Sp.contains(g * h * ginv):
                        unique_p = False
                        break
                    if not Sp.contains(ginv * h * g):
                        unique_p = False
                        break
                if not unique_p:
                    break
                    
            Sq = G.sylow_subgroup(q)
            unique_q = True
            for g in G.generators:
                ginv = ~g
                for h in Sq.generators:
                    if not Sq.contains(g * h * ginv):
                        unique_q = False
                        break
                    if not Sq.contains(ginv * h * g):
                        unique_q = False
                        break
                if not unique_q:
                    break
                    
            is_cyclic = False
            if order == p * q:
                if G.is_abelian:
                    if p != q:
                        is_cyclic = True
                    else:
                        if order <= 10000:
                            for g in G.elements:
                                if get_order(g) == order:
                                    is_cyclic = True
                                    break
            
            q_holds = unique_p and unique_q and is_cyclic
            
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is p * q",
    "H_2: p and q are prime numbers",
    "H_3: p is strictly less than q",
    "H_4: p does not divide q - 1",
    "¬Q: G does not have a unique normal Sylow p-subgroup, or does not have a unique normal Sylow q-subgroup, or is not isomorphic to the cyclic group of order pq"
]

N_HYP = 4
NEG_Q_INDEX = 4