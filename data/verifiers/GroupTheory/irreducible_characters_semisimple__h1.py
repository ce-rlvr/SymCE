import itertools
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def character_degrees(G):
    n_classes = len(G.conjugacy_classes())
    order = int(G.order())
    divisors = [d for d in range(1, order + 1) if order % d == 0]
    divisors.sort(reverse=True)
    
    def search(target, n_left, max_d_idx):
        if n_left == 0:
            if target == 0:
                return []
            else:
                return None
        if target < n_left:
            return None
        
        for i in range(max_d_idx, len(divisors)):
            d = divisors[i]
            if d*d * n_left < target:
                continue
            if d*d > target:
                continue
            res = search(target - d*d, n_left - 1, i)
            if res is not None:
                return [d] + res
        return None

    res = search(order, n_classes, 0)
    return res if res else [1]*n_classes

def get_product_multiset(S_list):
    degrees_list = [character_degrees(S) for S in S_list]
    prods = []
    for combo in itertools.product(*degrees_list):
        p = 1
        for d in combo:
            p *= d
        prods.append(p)
    return prods

def get_lcm(a, b):
    if hasattr(math, 'lcm'):
        return math.lcm(a, b)
    else:
        return abs(a * b) // math.gcd(a, b) if a and b else 0

def group_exponent(G):
    if int(G.order()) > 2000:
        return int(G.order())
    exp = 1
    for g in G.elements:
        exp = get_lcm(exp, int(g.order()))
    return exp

def direct_product(groups):
    if not groups:
        return PermutationGroup([Permutation(0)])
    
    total_degree = sum(G.degree for G in groups)
    if total_degree == 0:
        return PermutationGroup([Permutation(0)])
        
    full_generators = []
    offset = 0
    for G in groups:
        degree = G.degree
        if degree == 0:
            continue
        for g in G.generators:
            cycles = g.cyclic_form
            shifted_cycles = [[p + offset for p in cycle] for cycle in cycles]
            full_generators.append(Permutation(shifted_cycles, size=total_degree))
        offset += degree
        
    if not full_generators:
        return PermutationGroup([Permutation(total_degree - 1)])
        
    return PermutationGroup(full_generators)

def get_counts(seq):
    counts = {}
    for x in seq:
        counts[x] = counts.get(x, 0) + 1
    return counts

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            S_list = witness['S']
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2 and isinstance(witness[1], (list, tuple)):
                G, S_list = witness[0], witness[1]
            else:
                G = witness[0]
                S_list = witness[1:]
        else:
            G = witness
            S_list = []
            
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if not S_list:
            neg_q = len(G.conjugacy_classes()) > 1
        else:
            D_G = character_degrees(G)
            prods = get_product_multiset(S_list)
            
            cG = get_counts(D_G)
            cP = get_counts(prods)
            
            is_sub = True
            for k, v in cG.items():
                if cP.get(k, 0) < v:
                    is_sub = False
                    break
            
            if not is_sub:
                neg_q = True
            else:
                exp_G = group_exponent(G)
                exp_P = 1
                for S in S_list:
                    exp_P = get_lcm(exp_P, group_exponent(S))
                
                if exp_P % exp_G != 0:
                    neg_q = True
                else:
                    order_P = 1
                    for S in S_list:
                        order_P *= int(S.order())
                    
                    order_G = int(G.order())
                    if order_G > order_P:
                        neg_q = True
                    elif order_G == order_P:
                        P = direct_product(S_list)
                        if not G.is_isomorphic(P):
                            neg_q = True
                        else:
                            neg_q = False
                    else:
                        neg_q = False
                        
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Irr(X) denotes the set of irreducible complex characters of a group X",
    "¬Q: Not every irreducible character of G is of the form chi_1 x ... x chi_k"
]

N_HYP = 1
NEG_Q_INDEX = 1