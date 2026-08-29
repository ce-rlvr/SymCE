import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "H_2: N is a normal subgroup of G",
    "H_3: The index of N in G is finite",
    "not Q: The index of f(N) in H does not divide the index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def apply_f(f, x):
    if isinstance(f, dict):
        return f[x]
    else:
        return f(x)

def get_inv(x):
    try:
        return x**-1
    except Exception:
        return x.inv()

def check_h1(G, H, f):
    G_els = list(G.elements) if hasattr(G, 'elements') else list(G)
    H_els = list(H.elements) if hasattr(H, 'elements') else list(H)
    
    img = []
    for g in G_els:
        val = apply_f(f, g)
        if val not in img:
            img.append(val)
            
    if len(img) != len(H_els):
        return False
        
    for h in H_els:
        if h not in img:
            return False
            
    for g1 in G_els:
        for g2 in G_els:
            if apply_f(f, g1 * g2) != apply_f(f, g1) * apply_f(f, g2):
                return False
    return True

def check_h2(G, N):
    G_els = list(G.elements) if hasattr(G, 'elements') else list(G)
    N_els = list(N.elements) if hasattr(N, 'elements') else list(N)
        
    if not N_els:
        return False
        
    N_set = []
    for n in N_els:
        if n not in N_set:
            N_set.append(n)
            
    for n1 in N_els:
        for n2 in N_els:
            if n1 * n2 not in N_set:
                return False
    for n in N_els:
        if get_inv(n) not in N_set:
            return False
            
    for g in G_els:
        g_inv = get_inv(g)
        for n in N_els:
            if g * n * g_inv not in N_set:
                return False
    return True

def check_h3(G, N):
    try:
        if hasattr(G, 'order'):
            oG = G.order()
            if oG == float('inf') or str(oG) == 'oo':
                return False
        
        G_els = list(G.elements) if hasattr(G, 'elements') else list(G)
        N_els = list(N.elements) if hasattr(N, 'elements') else list(N)
        if len(N_els) == 0:
            return False
        return True
    except Exception:
        return False

def check_neg_Q(G, H, f, N):
    G_els = list(G.elements) if hasattr(G, 'elements') else list(G)
    N_els = list(N.elements) if hasattr(N, 'elements') else list(N)
    
    if len(N_els) == 0:
        return False
    idx_G_N = len(G_els) // len(N_els)
    
    f_N_set = []
    for n in N_els:
        val = apply_f(f, n)
        if val not in f_N_set:
            f_N_set.append(val)
            
    H_els = list(H.elements) if hasattr(H, 'elements') else list(H)
    if len(f_N_set) == 0:
        return False
    idx_H_fN = len(H_els) // len(f_N_set)
    
    if idx_H_fN == 0:
        return False
        
    return (idx_G_N % idx_H_fN) != 0

def conditions(witness):
    try:
        G, H, f, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_h1(G, H, f)
    except Exception:
        h1 = False
        
    try:
        h2 = check_h2(G, N)
    except Exception:
        h2 = False
        
    try:
        h3 = check_h3(G, N)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(G, H, f, N)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]