import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools

# Top-level setup for standard groups
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def check_H4(P, N, H_P=None):
    elements_P = list(P.generate_dimino())
    elements_N = list(N.generate_dimino())
    set_N = set(elements_N)
    
    # Check if N is normal in P
    for p_elem in elements_P:
        for n in elements_N:
            if (p_elem**-1 * n * p_elem) not in set_N:
                return False
                
    if H_P is not None and isinstance(H_P, PermutationGroup):
        if H_P.order() * N.order() != P.order():
            return False
        for h in H_P.generate_dimino():
            if not h.is_Identity and h in set_N:
                return False
        set_P = set(elements_P)
        for h in H_P.generate_dimino():
            if h not in set_P:
                return False
        return True
    else:
        target_order = len(elements_P) // len(elements_N)
        if target_order == 1:
            return True
        if target_order == len(elements_P):
            return True
            
        valid_elements = []
        for g in elements_P:
            if g.is_Identity:
                continue
            if g not in set_N and target_order % g.order() == 0:
                valid_elements.append(g)
                
        max_gens = int(math.log2(target_order))
        for r in range(1, max_gens + 1):
            for gens in itertools.combinations(valid_elements, r):
                try:
                    H = PermutationGroup(*gens)
                    if H.order() == target_order:
                        intersect_trivial = True
                        for h in H.generate_dimino():
                            if not h.is_Identity and h in set_N:
                                intersect_trivial = False
                                break
                        if intersect_trivial:
                            return True
                except Exception:
                    pass
        return False

def has_complement(G, N, check_normal=True):
    elements_G = list(G.generate_dimino())
    set_G = set(elements_G)
    elements_N = list(N.generate_dimino())
    set_N = set(elements_N)
    
    # Check if N <= G
    for n in elements_N:
        if n not in set_G:
            return False
            
    if check_normal:
        for g in elements_G:
            for n in elements_N:
                if (g**-1 * n * g) not in set_N:
                    return False
                    
    target_order = len(elements_G) // len(elements_N)
    if target_order == 1:
        return True
    if target_order == len(elements_G):
        return True
        
    valid_elements = []
    for g in elements_G:
        if g.is_Identity:
            continue
        if g not in set_N and target_order % g.order() == 0:
            valid_elements.append(g)
            
    max_gens = int(math.log2(target_order))
    for r in range(1, max_gens + 1):
        for gens in itertools.combinations(valid_elements, r):
            try:
                H = PermutationGroup(*gens)
                if H.order() == target_order:
                    intersect_trivial = True
                    for h in H.generate_dimino():
                        if not h.is_Identity and h in set_N:
                            intersect_trivial = False
                            break
                    if intersect_trivial:
                        return True
            except Exception:
                pass
    return False

def conditions(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        p = witness.get('p')
        P = witness.get('P')
        N = witness.get('N')
        H_P = witness.get('H_P', None)
    else:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, p, P, N = witness
                H_P = None
            elif len(witness) == 5:
                G, p, P, N, H_P = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
            
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and 0 < G.order() <= 2048
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if h1 and h2 and isinstance(P, PermutationGroup):
            elements_G = set(G.generate_dimino())
            p_is_subgroup = True
            for x in P.generate_dimino():
                if x not in elements_G:
                    p_is_subgroup = False
                    break
            if p_is_subgroup:
                order_G = G.order()
                expected_order = 1
                temp = order_G
                while temp % p == 0:
                    expected_order *= p
                    temp //= p
                h3 = (P.order() == expected_order)
    except Exception:
        h3 = False
        
    # H4: P = N \rtimes H_P for some H_P
    try:
        h4 = False
        if h3 and isinstance(N, PermutationGroup):
            elements_P = set(P.generate_dimino())
            n_is_subgroup = True
            for x in N.generate_dimino():
                if x not in elements_P:
                    n_is_subgroup = False
                    break
            if n_is_subgroup:
                h4 = check_H4(P, N, H_P)
    except Exception:
        h4 = False
        
    # neg_Q: G does NOT have a complement for N such that G = N \rtimes H
    try:
        neg_q = False
        if h1 and isinstance(N, PermutationGroup):
            has_comp = has_complement(G, N, check_normal=True)
            neg_q = not has_comp
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: There exists a complement of N in P, such that P = N rtimes H_P",
    "¬Q: There does not exist a complement of N in G such that G = N rtimes H"
]

N_HYP = 4
NEG_Q_INDEX = 4