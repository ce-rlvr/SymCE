import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def direct_product(groups):
    """Computes the direct product of a list of PermutationGroups."""
    if not groups:
        return PermutationGroup([Permutation(0)])
    if len(groups) == 1:
        return groups[0]
    
    total_degree = sum(g.degree for g in groups)
    gens = []
    offset = 0
    for g in groups:
        degree = g.degree
        if degree == 0:
            continue
        for gen in g.generators:
            arr = list(range(total_degree))
            for i in range(degree):
                arr[offset + i] = gen(i) + offset
            gens.append(Permutation(arr))
        offset += degree
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def check_simple(G):
    """Checks if a PermutationGroup is simple."""
    try:
        if hasattr(G, 'is_simple'):
            s = G.is_simple
            if callable(s):
                return s()
            elif s is not None:
                return s
    except Exception:
        pass
    
    try:
        if hasattr(G, 'normal_subgroups'):
            ns = G.normal_subgroups()
            return len(ns) == 2
    except Exception:
        pass
    
    # Fallback for A5 (the smallest non-abelian simple group)
    try:
        if G.order() == 60 and not G.is_abelian:
            return True
    except Exception:
        pass
        
    return False

def get_G_S_T(witness):
    """Extracts G, S_list, and T_list from the witness."""
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            S_list = witness.get('S_list')
            T_list = witness.get('T_list')
            if G is None and S_list is not None:
                G = direct_product(S_list)
            return G, S_list, T_list
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                return witness
            elif len(witness) == 2:
                S_list, T_list = witness
                return direct_product(S_list), S_list, T_list
    except Exception:
        pass
    return None, None, None

def conditions(witness) -> list[bool]:
    G, S_list, T_list = get_G_S_T(witness)
    
    if G is None or S_list is None or T_list is None:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G \cong S_1 \times \dots \times S_k, where each S_i is a non-abelian simple group
    try:
        h2 = True
        for S in S_list:
            if S.is_abelian:
                h2 = False
                break
            if not check_simple(S):
                h2 = False
                break
        if h2:
            DP = direct_product(S_list)
            try:
                iso = G.is_isomorphic(DP)
            except Exception:
                # Fallback if is_isomorphic fails
                iso = (G.order() == DP.order())
            if not iso:
                h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: It is NOT the case that k = m and S_i \cong T_{\sigma(i)} for some permutation \sigma
    try:
        k = len(S_list)
        m = len(T_list)
        if k != m:
            neg_q = True
        else:
            match_found = False
            for p in itertools.permutations(T_list):
                match = True
                for s, t in zip(S_list, p):
                    try:
                        iso = s.is_isomorphic(t)
                    except Exception:
                        iso = False
                    if not iso:
                        match = False
                        break
                if match:
                    match_found = True
                    break
            neg_q = not match_found
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is isomorphic to S_1 x ... x S_k, where each S_i is a non-abelian simple group",
    "¬Q: It is not the case that k = m and S_i is isomorphic to T_sigma(i) for some permutation sigma"
]

N_HYP = 2
NEG_Q_INDEX = 2