import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup

def _manual_direct_product(H, K):
    size_H = H.degree
    size_K = K.degree
    if size_H == 0: size_H = 1
    if size_K == 0: size_K = 1
    gens = []
    for g in H.generators:
        arr = list(g.array_form)
        if len(arr) < size_H: 
            arr += list(range(len(arr), size_H))
        arr += list(range(size_H, size_H + size_K))
        gens.append(Permutation(arr))
    for g in K.generators:
        arr = list(g.array_form)
        if len(arr) < size_K: 
            arr += list(range(len(arr), size_K))
        new_arr = list(range(size_H)) + [x + size_H for x in arr]
        gens.append(Permutation(new_arr))
    if not gens:
        return PermutationGroup([Permutation(size_H + size_K - 1)])
    return PermutationGroup(gens)

try:
    from sympy.combinatorics.group_constructs import DirectProduct
except ImportError:
    try:
        from sympy.combinatorics import DirectProduct
    except ImportError:
        DirectProduct = _manual_direct_product

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_direct_product(G, H, K):
    try:
        DP = DirectProduct(H, K)
        if G.order() == DP.order():
            if G.is_subgroup(DP) and DP.is_subgroup(G):
                return True
            if hasattr(G, 'is_isomorphic') and G.is_isomorphic(DP):
                return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            H = witness.get('H')
            K = witness.get('K')
            G = witness.get('G')
        else:
            H, K, G = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(K.is_solvable)
    except Exception:
        h1 = False

    try:
        h2 = is_direct_product(G, H, K)
    except Exception:
        h2 = False

    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a finite solvable group",
    "H_2: G is the external direct product of H and K",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2