import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def check_normal(G, N):
    if hasattr(G, 'is_normal'):
        try:
            res = G.is_normal(N)
            if res is not None:
                return bool(res)
        except Exception:
            pass
            
    if hasattr(N, 'is_normal'):
        try:
            res = N.is_normal(G)
            if res is not None:
                return bool(res)
        except Exception:
            pass

    try:
        if hasattr(N, 'is_subgroup') and not N.is_subgroup(G):
            return False
        if hasattr(G, 'generators') and hasattr(N, 'generators'):
            for g in G.generators:
                for n in N.generators:
                    if (~g * n * g) not in N:
                        return False
            return True
    except Exception:
        pass

    if hasattr(G, 'is_normal_subgroup'):
        try:
            return bool(G.is_normal_subgroup(N))
        except Exception:
            pass
            
    return False

def check_fg(G):
    if hasattr(G, 'is_finitely_generated'):
        return bool(G.is_finitely_generated)
    
    class_name = type(G).__name__
    if class_name in ('PermutationGroup', 'FpGroup', 'FreeGroup'):
        return True
        
    if hasattr(G, 'generators') and hasattr(G, 'is_subgroup'):
        return True
        
    return False

def check_quotient_fg(G, N):
    if hasattr(G, 'quotient_is_finitely_generated'):
        try:
            return bool(G.quotient_is_finitely_generated(N))
        except Exception:
            pass
    if hasattr(G, 'quotient'):
        try:
            Q = G.quotient(N)
            return check_fg(Q)
        except Exception:
            pass
    if check_fg(G):
        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
        else:
            G = witness.G
            N = witness.N
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_normal(G, N)
    except Exception:
        h1 = False
        
    try:
        h2 = check_fg(N)
    except Exception:
        h2 = False
        
    try:
        h3 = check_quotient_fg(G, N)
    except Exception:
        h3 = False
        
    try:
        neg_q = not check_fg(G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a finitely generated group",
    "H_3: The quotient group G/N is a finitely generated group",
    "¬Q: G is not a finitely generated group"
]

N_HYP = 3
NEG_Q_INDEX = 3