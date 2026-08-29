import math
from itertools import combinations
import sympy
from sympy.combinatorics import Permutation, PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def same_group(G1, G2):
    try:
        if G1.order() != G2.order(): 
            return False
        for g in G1.generators:
            if g not in G2: 
                return False
        return True
    except Exception:
        return False

def is_subgroup(N, G):
    try:
        for g in N.generators:
            if g not in G: 
                return False
        return True
    except Exception:
        return False

def get_canonical_factors(S_list):
    factors = []
    offset = 0
    total_degree = sum(S.degree for S in S_list)
    for S in S_list:
        gens = []
        for g in S.generators:
            images = list(range(total_degree))
            for i in range(S.degree):
                images[offset + i] = offset + g(i)
            gens.append(Permutation(images))
        if gens:
            factors.append(PermutationGroup(gens))
        else:
            factors.append(PermutationGroup([Permutation(total_degree - 1)]))
        offset += S.degree
    return factors

def is_canonical_subgroup(N, S_list, G):
    factors = get_canonical_factors(S_list)
    for r in range(len(factors) + 1):
        for subset in combinations(factors, r):
            gens = []
            for f in subset:
                gens.extend(f.generators)
            if not gens:
                if N.order() == 1:
                    return True
                continue
            
            H = PermutationGroup(gens)
            if same_group(N, H):
                return True
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        S_list, G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: S_1, S_2, ..., S_n is a finite collection of non-abelian simple groups
    try:
        h1 = False
        if isinstance(S_list, (list, tuple)) and len(S_list) > 0:
            h1_ok = True
            for S in S_list:
                if S.is_abelian:
                    h1_ok = False
                    break
                if S.derived_subgroup().order() != S.order():
                    h1_ok = False
                    break
                order = S.order()
                is_simple = False
                # Check known orders of small non-abelian simple groups
                if order in [math.factorial(n)//2 for n in range(5, 15)]:
                    is_simple = True
                elif order in [60, 168, 360, 504, 660, 1092, 2520, 3420, 4080, 5616, 6048, 7920, 9504]:
                    is_simple = True
                
                if not is_simple:
                    h1_ok = False
                    break
            h1 = h1_ok
    except Exception:
        h1 = False

    # H_2: G is the direct product S_1 x S_2 x ... x S_n
    try:
        if len(S_list) == 1:
            DP = S_list[0]
        else:
            DP = DirectProduct(*S_list)
        h2 = same_group(G, DP)
    except Exception:
        h2 = False

    # ¬Q: N does not correspond to the internal direct product of a subcollection of the groups S_i within G
    try:
        neg_q = False
        if is_subgroup(N, G):
            if not is_canonical_subgroup(N, S_list, G):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_1, S_2, ..., S_n is a finite collection of non-abelian simple groups",
    "H_2: G is the direct product S_1 x S_2 x ... x S_n",
    "¬Q: N does not correspond to the internal direct product of a subcollection of the groups S_i within G"
]

N_HYP = 2
NEG_Q_INDEX = 2