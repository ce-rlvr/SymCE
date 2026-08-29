import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
import sympy.ntheory as nt
from sympy.matrices import eye, zeros

# Top-level setup
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
    def get_order(grp):
        order = grp.order
        if callable(order):
            return order()
        return order

    def check_h1():
        try:
            G, p, P, S = witness
            if not nt.isprime(p): 
                return False
            return get_order(G) % p == 0
        except Exception:
            return False

    def check_h2():
        try:
            G, p, P, S = witness
            if not all(g in G for g in P.generators): 
                return False
            order_G = get_order(G)
            k = 0
            temp = order_G
            while temp % p == 0 and temp > 0:
                k += 1
                temp //= p
            return get_order(P) == p**k
        except Exception:
            return False

    def check_h3():
        try:
            G, p, P, S = witness
            if hasattr(G, 'all_sylow_p_subgroups'):
                all_syls = G.all_sylow_p_subgroups(p)
                if len(S) != len(all_syls): 
                    return False
                for Q in S:
                    found = False
                    for U in all_syls:
                        if get_order(Q) == get_order(U) and all(g in U for g in Q.generators):
                            found = True
                            break
                    if not found: 
                        return False
                return True
            
            order_G = get_order(G)
            k = 0
            temp = order_G
            while temp % p == 0 and temp > 0:
                k += 1
                temp //= p
            target_order = p**k
            
            S_unique = []
            for Q in S:
                if not all(g in G for g in Q.generators): 
                    return False
                if get_order(Q) != target_order: 
                    return False
                is_dup = False
                for U in S_unique:
                    if all(g in U for g in Q.generators):
                        is_dup = True
                        break
                if is_dup: 
                    return False
                S_unique.append(Q)
                
            if len(S) == 0:
                return False
                
            for Q in S_unique:
                for g in G.generators:
                    conj1_gens = [~g * x * g for x in Q.generators]
                    conj2_gens = [g * x * ~g for x in Q.generators]
                    
                    found1 = False
                    found2 = False
                    for U in S_unique:
                        if not found1 and all(x in U for x in conj1_gens):
                            found1 = True
                        if not found2 and all(x in U for x in conj2_gens):
                            found2 = True
                        if found1 and found2:
                            break
                    if not found1 and not found2:
                        return False
            return True
        except Exception:
            return False

    def check_h4():
        try:
            G, p, P, S = witness
            for Q in S:
                for g in P.generators:
                    conj1_gens = [~g * x * g for x in Q.generators]
                    conj2_gens = [g * x * ~g for x in Q.generators]
                    
                    found1 = False
                    found2 = False
                    for U in S:
                        if not found1 and all(x in U for x in conj1_gens):
                            found1 = True
                        if not found2 and all(x in U for x in conj2_gens):
                            found2 = True
                        if found1 and found2:
                            break
                    if not found1 and not found2:
                        return False
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            G, p, P, S = witness
            return len(S) % p != 1
        except Exception:
            return False

    return [check_h1(), check_h2(), check_h3(), check_h4(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: p is a prime dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: S is the set of all Sylow p-subgroups of G",
    "H_4: P acts on S by conjugation",
    "¬Q: The number of Sylow p-subgroups of G (the cardinality of S) is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4