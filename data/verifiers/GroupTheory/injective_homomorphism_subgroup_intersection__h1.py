import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(S):
    if hasattr(S, 'generate'):
        return set(S.generate())
    elif hasattr(S, 'elements'):
        return set(S.elements)
    else:
        return set(S)

def in_group(x, G):
    if hasattr(G, 'contains'):
        return G.contains(x)
    try:
        if x in G:
            return True
    except Exception:
        pass
    return x in get_elements(G)

def conditions(witness):
    try:
        G = witness['G']
        A = witness['A']
        B = witness['B']
        
        def is_subgroup(S, G):
            if hasattr(S, 'is_subgroup') and hasattr(G, 'is_group'):
                try:
                    return S.is_subgroup(G)
                except Exception:
                    pass
            S_set = get_elements(S)
            if not S_set: 
                return False
            for x in S_set:
                if not in_group(x, G): 
                    return False
            for x in S_set:
                for y in S_set:
                    if (x * y) not in S_set: 
                        return False
            return True
            
        h1 = is_subgroup(A, G) and is_subgroup(B, G)
    except Exception:
        h1 = False
        
    try:
        A = witness['A']
        B = witness['B']
        f = witness['f']
        
        A_set = get_elements(A)
        B_set = get_elements(B)
        A_cap_B = A_set.intersection(B_set)
        
        def eval_f(func, x):
            if callable(func):
                return func(x)
            elif isinstance(func, dict):
                return func[x]
            else:
                for k, v in func:
                    if k == x:
                        return v
                raise KeyError(x)
                
        def make_hashable(val):
            if isinstance(val, list):
                return tuple(val)
            elif isinstance(val, set):
                return frozenset(val)
            elif isinstance(val, dict):
                return frozenset(val.items())
            return val

        f_A_cap_B = set(make_hashable(eval_f(f, x)) for x in A_cap_B)
        f_A = set(make_hashable(eval_f(f, x)) for x in A_set)
        f_B = set(make_hashable(eval_f(f, x)) for x in B_set)
            
        f_A_cap_f_B = f_A.intersection(f_B)
        
        neg_q = f_A_cap_B != f_A_cap_f_B
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are subgroups of G",
    "¬Q: f(A \\cap B) != f(A) \\cap f(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1