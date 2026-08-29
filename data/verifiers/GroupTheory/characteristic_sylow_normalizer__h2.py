import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_normalizer(G, P):
    P_elements = set(P.generate())
    norm_gens = []
    for g in G.generate():
        normalizes = True
        for p in P.generators:
            if g * p * ~g not in P_elements:
                normalizes = False
                break
        if normalizes:
            norm_gens.append(g)
    if not norm_gens:
        id_G = G.generators[0]**0 if G.generators else Permutation()
        return PermutationGroup(id_G)
    return PermutationGroup(*norm_gens)

def is_characteristic(N, P):
    gens = N.generators
    if N.order() == 1:
        return True
        
    id_N = gens[0]**0
    elements = list(N.generate())
    P_elements = set(P.generate())
    n_elements = len(elements)
    
    for t in itertools.product(elements, repeat=len(gens)):
        mapping = {id_N: id_N}
        queue = [id_N]
        head = 0
        is_homo = True
        
        while head < len(queue):
            u = queue[head]
            head += 1
            for i, g in enumerate(gens):
                v = u * g
                mapped_v = mapping[u] * t[i]
                if v in mapping:
                    if mapping[v] != mapped_v:
                        is_homo = False
                        break
                else:
                    mapping[v] = mapped_v
                    queue.append(v)
            if not is_homo:
                break
                
        if is_homo and len(set(mapping.values())) == n_elements:
            for p in P.generators:
                if mapping[p] not in P_elements:
                    return False
    return True

def conditions(witness):
    try:
        G, P = witness
        h1 = isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and P.is_subgroup(G)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            N = get_normalizer(G, P)
            neg_q = not is_characteristic(N, P)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and P is a subgroup of G",
    "¬Q: P is not a characteristic subgroup of its normalizer N_G(P)"
]

N_HYP = 1
NEG_Q_INDEX = 1