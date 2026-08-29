import sympy
from sympy import S
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

QQ = S.Rationals
ZZ = S.Integers
RR = S.Reals
CC = S.Complexes

def check_attr(obj, attr):
    if hasattr(obj, attr):
        val = getattr(obj, attr)
        return val() if callable(val) else val
    return None

def is_abelian_group(G):
    if isinstance(G, tuple):
        return all(is_abelian_group(g) for g in G)
    if hasattr(G, 'sets') and isinstance(G.sets, tuple):
        return all(is_abelian_group(g) for g in G.sets)
    if isinstance(G, str):
        return G.lower() in ['q', 'r', 'c', 'z', 'rationals', 'reals', 'complexes', 'integers', 'qq', 'zz', 'rr', 'cc']
    if G in (S.Rationals, S.Reals, S.Complexes, S.Integers):
        return True
    if G.__class__.__name__ in ['RationalField', 'RealField', 'ComplexField', 'IntegerRing']:
        return True
    
    val = check_attr(G, 'is_abelian_group')
    if val is not None: return bool(val)
    
    val = check_attr(G, 'is_abelian')
    if val is not None: return bool(val)
    
    return False

def is_torsion_free(G):
    if isinstance(G, tuple):
        return all(is_torsion_free(g) for g in G)
    if hasattr(G, 'sets') and isinstance(G.sets, tuple):
        return all(is_torsion_free(g) for g in G.sets)
    if isinstance(G, str):
        return G.lower() in ['q', 'r', 'c', 'z', 'rationals', 'reals', 'complexes', 'integers', 'qq', 'zz', 'rr', 'cc']
    if G in (S.Rationals, S.Reals, S.Complexes, S.Integers):
        return True
    if G.__class__.__name__ in ['RationalField', 'RealField', 'ComplexField', 'IntegerRing']:
        return True
    
    val = check_attr(G, 'is_torsion_free')
    if val is not None: return bool(val)
    
    try:
        if hasattr(G, 'order'):
            return G.order() == 1
    except Exception:
        pass
        
    try:
        if hasattr(G, 'elements'):
            return len(list(G.elements)) == 1
    except Exception:
        pass
        
    return False

def is_free_abelian(G):
    if isinstance(G, tuple):
        return all(is_free_abelian(g) for g in G)
    if hasattr(G, 'sets') and isinstance(G.sets, tuple):
        return all(is_free_abelian(g) for g in G.sets)
    if isinstance(G, str):
        return G.lower() in ['z', 'integers', 'zz']
    if G is S.Integers:
        return True
    if G.__class__.__name__ == 'IntegerRing':
        return True
    if G in (S.Rationals, S.Reals, S.Complexes):
        return False
    if G.__class__.__name__ in ['RationalField', 'RealField', 'ComplexField']:
        return False
        
    val = check_attr(G, 'is_free_abelian')
    if val is not None: return bool(val)
    
    try:
        if hasattr(G, 'order'):
            return G.order() == 1
    except Exception:
        pass
        
    try:
        if hasattr(G, 'elements'):
            return len(list(G.elements)) == 1
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        h1 = is_abelian_group(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_torsion_free(witness)
    except Exception:
        h2 = False

    try:
        neg_q = not is_free_abelian(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G is torsion-free",
    "¬Q: G is not a free abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2