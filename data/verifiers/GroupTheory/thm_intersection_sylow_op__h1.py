import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'generate') and callable(group.generate):
        return frozenset(group.generate())
    elif hasattr(group, 'elements'):
        return frozenset(group.elements)
    else:
        return frozenset(group)

def conditions(witness):
    try:
        G, p, S = witness
        S = list(S)
    except Exception:
        return [False, False, False]

    # H1: p is a prime number dividing the order of G
    try:
        h1 = bool(sympy.ntheory.isprime(p) and (G.order() % p == 0))
    except Exception:
        h1 = False

    # H2: S is the set of all Sylow p-subgroups of G
    try:
        if hasattr(G, 'sylow_subgroup'):
            P = G.sylow_subgroup(p)
            P_elems = get_elements(P)
        else:
            P_elems = get_elements(S[0])

        G_elems = get_elements(G)
        
        all_sylows = set()
        for g in G_elems:
            conj_elems = frozenset([g * x * ~g for x in P_elems])
            all_sylows.add(conj_elems)
            
        S_sets = set()
        for sub in S:
            S_sets.add(get_elements(sub))
            
        h2 = bool(S_sets == all_sylows)
        
        order_G = G.order()
        p_power = 1
        temp = order_G
        if temp > 0:
            while temp % p == 0:
                p_power *= p
                temp //= p
        if len(P_elems) != p_power:
            h2 = False
            
    except Exception:
        h2 = False

    # Conclusion: The intersection of all subgroups in S is the unique largest normal p-subgroup of G, denoted O_p(G)
    try:
        intersection_elems = None
        for sub in S:
            elems = get_elements(sub)
            if intersection_elems is None:
                intersection_elems = elems
            else:
                intersection_elems = intersection_elems.intersection(elems)
                
        if intersection_elems is None:
            intersection_elems = get_elements(G)
            
        normal_p_subgroups = []
        for N in G.normal_subgroups():
            N_order = N.order()
            is_p_group = True
            temp = N_order
            if temp <= 0:
                is_p_group = False
            else:
                while temp > 1:
                    if temp % p != 0:
                        is_p_group = False
                        break
                    temp //= p
            if is_p_group:
                normal_p_subgroups.append(N)
                
        if not normal_p_subgroups:
            G_elems = get_elements(G)
            identity = None
            for e in G_elems:
                if e * e == e:
                    identity = e
                    break
            OpG_elems = frozenset([identity])
        else:
            max_order = max([N.order() for N in normal_p_subgroups])
            largest_normal_p_subgroups = [N for N in normal_p_subgroups if N.order() == max_order]
            OpG = largest_normal_p_subgroups[0]
            OpG_elems = get_elements(OpG)
            
        q = bool(intersection_elems == OpG_elems)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "H_2: S is the set of all Sylow p-subgroups of G",
    "¬Q: The intersection of all subgroups in S is not the unique largest normal p-subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2