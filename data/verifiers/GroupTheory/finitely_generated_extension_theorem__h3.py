import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def get_bool_prop(obj, prop_name, *args):
    if isinstance(obj, dict) and prop_name in obj:
        val = obj[prop_name]
        try:
            if callable(val):
                return bool(val(*args))
            return bool(val)
        except Exception:
            return False
    if hasattr(obj, prop_name):
        try:
            val = getattr(obj, prop_name)
            if callable(val):
                return bool(val(*args))
            return bool(val)
        except Exception:
            pass
    return None

def check_is_group(G):
    res = get_bool_prop(G, 'is_group')
    if res is not None: 
        return res
    
    import sympy.combinatorics as sc
    classes = []
    if hasattr(sc, 'PermutationGroup'): classes.append(sc.PermutationGroup)
    if hasattr(sc, 'FpGroup'): classes.append(sc.FpGroup)
    if hasattr(sc, 'FreeGroup'): classes.append(sc.FreeGroup)
    
    if classes and isinstance(G, tuple(classes)):
        return True
    return False

def check_is_normal_subgroup(N, G):
    res = get_bool_prop(N, 'is_normal_subgroup', G)
    if res is not None: return res
    res = get_bool_prop(G, 'is_normal_subgroup', N)
    if res is not None: return res
    res = get_bool_prop(N, 'is_normal', G)
    if res is not None: return res
    res = get_bool_prop(G, 'is_normal', N)
    if res is not None: return res
    
    try:
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            if hasattr(N, 'is_normal'):
                return bool(N.is_normal(G))
    except Exception:
        pass
    return False

def check_is_finitely_generated(G):
    res = get_bool_prop(G, 'is_finitely_generated')
    if res is not None: 
        return res
    
    import sympy.combinatorics as sc
    classes = []
    if hasattr(sc, 'PermutationGroup'): classes.append(sc.PermutationGroup)
    if hasattr(sc, 'FpGroup'): classes.append(sc.FpGroup)
    if hasattr(sc, 'FreeGroup'): classes.append(sc.FreeGroup)
    
    if classes and isinstance(G, tuple(classes)):
        return True
    return False

def check_quotient_is_finitely_generated(G, N):
    res = get_bool_prop(G, 'quotient_is_finitely_generated', N)
    if res is not None: 
        return res
    
    Q = None
    try:
        if isinstance(G, dict) and 'quotient' in G:
            val = G['quotient']
            Q = val(N) if callable(val) else val
        elif hasattr(G, 'quotient'):
            val = G.quotient
            Q = val(N) if callable(val) else val
        elif hasattr(G, 'quotient_group'):
            val = G.quotient_group
            Q = val(N) if callable(val) else val
    except Exception:
        pass
        
    if Q is not None:
        return check_is_finitely_generated(Q)
        
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict) and 'G' in witness and 'N' in witness:
            G = witness['G']
            N = witness['N']
        elif hasattr(witness, 'G') and hasattr(witness, 'N'):
            G = witness.G
            N = witness.N
        else:
            G, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_is_group(G)
    except Exception:
        h1 = False
        
    try:
        h2 = check_is_group(N) and check_is_normal_subgroup(N, G)
    except Exception:
        h2 = False
        
    try:
        h3 = check_quotient_is_finitely_generated(G, N)
    except Exception:
        h3 = False
        
    try:
        neg_q = not check_is_finitely_generated(G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: The quotient group G/N is a finitely generated group",
    "¬Q: G is not a finitely generated group"
]

N_HYP = 3
NEG_Q_INDEX = 3