import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N, H, p = witness
    except Exception:
        return [False, False, False, False]
        
    def get_identity(group):
        try:
            e = next(group.generate())
            return e * ~e
        except StopIteration:
            return Permutation()

    # H1: G is a finite group that is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        h1_ok = False
        if hasattr(G, 'generators') and hasattr(N, 'generators') and hasattr(H, 'generators'):
            n_sub = all(n in G for n in N.generators)
            h_sub = all(h in G for h in H.generators)
            
            if n_sub and h_sub:
                n_normal = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            n_normal = False
                            break
                    if not n_normal:
                        break
                
                if n_normal:
                    intersect_trivial = True
                    identity = get_identity(G)
                    for h in H.generate():
                        if h != identity and h in N:
                            intersect_trivial = False
                            break
                    
                    if intersect_trivial:
                        if G.order() == N.order() * H.order():
                            h1_ok = True
    except Exception:
        h1_ok = False

    # H2: p is a prime number
    try:
        h2_ok = sympy.isprime(p)
    except Exception:
        h2_ok = False

    # H3: The order of H is coprime to p
    try:
        h3_ok = math.gcd(int(H.order()), int(p)) == 1
    except Exception:
        h3_ok = False

    # ¬Q: N is not the internal direct product of C_N(H) and the mixed commutator subgroup
    try:
        CN_H = []
        for n in N.generate():
            if all(n * h == h * n for h in H.generators):
                CN_H.append(n)
                
        gens_comm = []
        for n in N.generate():
            for h in H.generate():
                gens_comm.append(~n * ~h * n * h)
        if not gens_comm:
            gens_comm = [get_identity(N)]
        
        comm_NH_group = PermutationGroup(gens_comm)
        comm_NH = list(comm_NH_group.generate())
        
        CN_H_set = set(CN_H)
        comm_NH_set = set(comm_NH)
        
        is_direct_product = True
        
        for c in CN_H:
            for n in N.generators:
                if (n * c * ~n) not in CN_H_set:
                    is_direct_product = False
                    break
            if not is_direct_product:
                break
                
        if is_direct_product:
            for c in comm_NH:
                for n in N.generators:
                    if (n * c * ~n) not in comm_NH_set:
                        is_direct_product = False
                        break
                if not is_direct_product:
                    break
                    
        if is_direct_product:
            if len(CN_H_set.intersection(comm_NH_set)) != 1:
                is_direct_product = False
                
        if is_direct_product:
            if len(CN_H) * len(comm_NH) != N.order():
                is_direct_product = False
                
        neg_q = not is_direct_product
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group that is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: p is a prime number",
    "H_3: The order of H is coprime to p",
    "¬Q: N is not the internal direct product of C_N(H) and the mixed commutator subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3