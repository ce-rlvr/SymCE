import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
        G, p, S = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False
        
    # neg_Q: The intersection of all subgroups in S is NOT O_p(G)
    try:
        # Compute O_p(G) as the intersection of all Sylow p-subgroups
        P = G.sylow_subgroup(p)
        P_elements = set(P.elements)
        O_p_elements = set(G.elements)
        for g in G.elements:
            conj_P = {g * x * ~g for x in P_elements}
            O_p_elements = O_p_elements.intersection(conj_P)
            
        # Compute the intersection of all subgroups in S
        S_list = list(S)
        if not S_list:
            S_intersection = set(G.elements)
        else:
            def get_elems(H):
                if hasattr(H, 'elements'):
                    return set(H.elements)
                return set(H)
            
            S_intersection = get_elems(S_list[0])
            for H in S_list[1:]:
                S_intersection = S_intersection.intersection(get_elems(H))
                
        neg_q = (S_intersection != O_p_elements)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "¬Q: The intersection of all subgroups in S is not O_p(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2