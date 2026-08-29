import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_perfect(G):
    try:
        return G.derived_subgroup().order() == G.order()
    except AttributeError:
        G_elems = list(G.generate())
        commutators = []
        for x in G_elems:
            for y in G_elems:
                commutators.append(x * y * x**-1 * y**-1)
        D = PermutationGroup(commutators)
        return D.order() == G.order()

def is_nonabelian_simple(G):
    if G.is_abelian: 
        return False
    if not is_perfect(G): 
        return False
    # Check against known orders of small non-abelian simple groups
    if G.order() in (60, 168, 360, 504, 660, 1092):
        return True
    return False

def is_internal_direct_product(G, S_list):
    if not S_list:
        return False
    
    G_elems = frozenset(G.generate())
    
    # Check if all S are subgroups
    for S in S_list:
        if not all(g in G_elems for g in S.generators):
            return False
            
    # Check if they commute pairwise
    for i in range(len(S_list)):
        for j in range(i + 1, len(S_list)):
            for g1 in S_list[i].generators:
                for g2 in S_list[j].generators:
                    if g1 * g2 != g2 * g1:
                        return False
                        
    # Check if product of orders equals G.order()
    prod_order = 1
    for S in S_list:
        prod_order *= S.order()
    if prod_order != G.order():
        return False
        
    return True

def get_all_sylow(S, p):
    P0 = S.sylow_subgroup(p)
    P0_elems = list(P0.generate())
    seen = set()
    sylows = []
    for g in S.generate():
        conj_elems = frozenset([g * x * g**-1 for x in P0_elems])
        if conj_elems not in seen:
            seen.add(conj_elems)
            sylows.append(conj_elems)
    return sylows

def check_conclusion(G, p, P, S_list):
    P_elems = frozenset(P.generate())
    
    sylow_lists = []
    for S in S_list:
        sylows = get_all_sylow(S, p)
        sylow_lists.append(sylows)
        
    count = 0
    for combo in itertools.product(*sylow_lists):
        id_elem = list(G.generate())[0] ** 0
        prod_elems = {id_elem}
        
        for P_i_elems in combo:
            new_prod = set()
            for x in prod_elems:
                for y in P_i_elems:
                    new_prod.add(x * y)
            prod_elems = new_prod
            
        if frozenset(prod_elems) == P_elems:
            count += 1
            
    return count == 1

def conditions(witness):
    """
    witness is expected to be a tuple: (G, p, P, S_list)
    where:
      - G is a PermutationGroup
      - p is an integer (prime)
      - P is a PermutationGroup
      - S_list is a list of PermutationGroups
    """
    try:
        G, p, P, S_list = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a semisimple finite group such that G = S_1 x ... x S_k where each S_i is a non-abelian simple group
    try:
        h1 = True
        if not is_internal_direct_product(G, S_list):
            h1 = False
        for S in S_list:
            if not is_nonabelian_simple(S):
                h1 = False
    except Exception:
        h1 = False
        
    # H_2: p is a prime dividing the order of G
    try:
        h2 = bool(sympy.isprime(p) and (G.order() % p == 0))
    except Exception:
        h2 = False
        
    # neg_Q: P CANNOT be uniquely expressed as P_1 x ... x P_k where each P_i is a Sylow p-subgroup of S_i
    try:
        q_holds = check_conclusion(G, p, P, S_list)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group such that G = S_1 x ... x S_k where each S_i is a non-abelian simple group",
    "H_2: p is a prime dividing the order of G",
    "¬Q: P cannot be uniquely expressed as P_1 x ... x P_k where each P_i is a Sylow p-subgroup of S_i"
]

N_HYP = 2
NEG_Q_INDEX = 2