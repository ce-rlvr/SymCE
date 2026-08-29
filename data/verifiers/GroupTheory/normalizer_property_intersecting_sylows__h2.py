import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def get_elements(group_or_list):
    if hasattr(group_or_list, 'generate'):
        return set(group_or_list.generate())
    else:
        return set(PermutationGroup(group_or_list).generate())

def is_subgroup(sub_gens, G):
    for g in sub_gens:
        try:
            if not G.contains(g):
                return False
        except Exception:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, P, Q, p = witness
        elif len(witness) == 3:
            G, P, Q = witness
            P_elements = get_elements(P)
            order_P = len(P_elements)
            factors = factorint(order_P)
            if len(factors) == 1:
                p = list(factors.keys())[0]
            else:
                p = 0
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: P and Q are distinct Sylow p-subgroups of G
    try:
        if not isprime(p):
            h2 = False
        else:
            order_G = G.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            sylow_order = p**k
            
            P_gens = P.generators if hasattr(P, 'generators') else P
            Q_gens = Q.generators if hasattr(Q, 'generators') else Q
            
            P_in_G = is_subgroup(P_gens, G)
            Q_in_G = is_subgroup(Q_gens, G)
            
            P_elements = get_elements(P)
            Q_elements = get_elements(Q)
            
            is_distinct = P_elements != Q_elements
            is_sylow_P = len(P_elements) == sylow_order
            is_sylow_Q = len(Q_elements) == sylow_order
            
            h2 = P_in_G and Q_in_G and is_distinct and is_sylow_P and is_sylow_Q
    except Exception:
        h2 = False
        
    # neg_Q: P \cap Q is NOT a strictly proper subgroup of N_P(P \cap Q) OR NOT a strictly proper subgroup of N_Q(P \cap Q)
    try:
        P_elements = get_elements(P)
        Q_elements = get_elements(Q)
            
        R_elements = P_elements.intersection(Q_elements)
        
        N_P_R = set()
        for x in P_elements:
            normalizes = True
            for r in R_elements:
                if (x * r * ~x) not in R_elements:
                    normalizes = False
                    break
            if normalizes:
                N_P_R.add(x)
                
        N_Q_R = set()
        for x in Q_elements:
            normalizes = True
            for r in R_elements:
                if (x * r * ~x) not in R_elements:
                    normalizes = False
                    break
            if normalizes:
                N_Q_R.add(x)
                
        # R is strictly proper in N_P(R) iff len(R) < len(N_P(R)).
        # Thus, it fails to be strictly proper iff len(R) == len(N_P(R)).
        neg_q = (len(R_elements) == len(N_P_R)) or (len(R_elements) == len(N_Q_R))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P and Q are distinct Sylow p-subgroups of G",
    "¬Q: P \\cap Q is not a strictly proper subgroup of N_P(P \\cap Q) or not a strictly proper subgroup of N_Q(P \\cap Q)"
]

N_HYP = 2
NEG_Q_INDEX = 2