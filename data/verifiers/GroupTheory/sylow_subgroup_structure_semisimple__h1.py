import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory as nt
import itertools

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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, p, P, S_list)
    where S_list is a list of groups S_1, ..., S_k.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        G, p, P, S_list = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime dividing the order of G
    try:
        h1 = bool(nt.isprime(p) and (G.order() % p == 0))
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if frozenset(P.elements).issubset(frozenset(G.elements)):
            order_G = G.order()
            a = 0
            while order_G % p == 0:
                a += 1
                order_G //= p
            if P.order() == p**a:
                h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: P cannot be uniquely expressed as P_1 x ... x P_k where P_i is a Sylow p-subgroup of S_i
    try:
        sylows_per_S = []
        for S in S_list:
            P0 = S.sylow_subgroup(p)
            sylows = []
            sylows_set = set()
            if P0.order() == 1:
                sylows.append(P0)
            else:
                for g in S.elements:
                    gens = [g * gen * ~g for gen in P0.generators]
                    P_conj = PermutationGroup(gens)
                    elems = frozenset(P_conj.elements)
                    if elems not in sylows_set:
                        sylows_set.add(elems)
                        sylows.append(P_conj)
            sylows_per_S.append(sylows)
            
        valid_expressions = 0
        P_elems = frozenset(P.elements)
        
        for P_tuple in itertools.product(*sylows_per_S):
            # 1. Check if all P_i are subgroups of P
            is_subgroup = True
            for Pi in P_tuple:
                if not frozenset(Pi.elements).issubset(P_elems):
                    is_subgroup = False
                    break
            if not is_subgroup:
                continue
                
            # 2. Check if elements of P_i and P_j commute for i != j
            commutes = True
            for i in range(len(P_tuple)):
                for j in range(i + 1, len(P_tuple)):
                    for g1 in P_tuple[i].generators:
                        for g2 in P_tuple[j].generators:
                            if g1 * g2 != g2 * g1:
                                commutes = False
                                break
                        if not commutes: break
                if not commutes: break
            if not commutes:
                continue
                
            # 3. Check if the internal direct product equals P
            prod_orders = 1
            all_gens = []
            for Pi in P_tuple:
                prod_orders *= Pi.order()
                all_gens.extend(Pi.generators)
                
            if prod_orders != P.order():
                continue
                
            if not all_gens:
                gen_order = 1
            else:
                gen_group = PermutationGroup(all_gens)
                gen_order = gen_group.order()
                
            if gen_order == P.order():
                valid_expressions += 1
                
            if valid_expressions > 1:
                break
                
        neg_q = (valid_expressions != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: P cannot be uniquely expressed as P_1 x ... x P_k where P_i is a Sylow p-subgroup of S_i"
]

N_HYP = 2
NEG_Q_INDEX = 2