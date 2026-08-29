import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    if hasattr(G, 'generate'):
        return list(G.generate())
    elif hasattr(G, 'elements'):
        return list(G.elements)
    else:
        return list(G)

def is_group(els):
    if not els:
        return False
    e = None
    for g in els:
        if all(g * x == x and x * g == x for x in els):
            e = g
            break
    if e is None:
        return False
    for a in els:
        for b in els:
            if a * b not in els:
                return False
    for a in els:
        has_inv = False
        for b in els:
            if a * b == e and b * a == e:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def check_H1(G, H, f):
    try:
        G_els = get_elements(G)
        H_els = get_elements(H)
        
        if not is_group(G_els) or not is_group(H_els):
            return False
            
        if not isinstance(f, dict):
            if callable(f):
                f_dict = {}
                for g in G_els:
                    f_dict[g] = f(g)
                f = f_dict
            else:
                return False
                
        for g in G_els:
            if g not in f:
                return False
            if f[g] not in H_els:
                return False
                
        for g1 in G_els:
            for g2 in G_els:
                if f[g1 * g2] != f[g1] * f[g2]:
                    return False
                    
        image = []
        for g in G_els:
            if f[g] not in image:
                image.append(f[g])
        if len(image) != len(H_els):
            return False
            
        return True
    except Exception:
        return False

def check_H2(G, N):
    try:
        G_els = get_elements(G)
        N_els = get_elements(N)
        
        if not is_group(G_els):
            return False
            
        for n in N_els:
            if n not in G_els:
                return False
                
        if not is_group(N_els):
            return False
            
        e = None
        for g in G_els:
            if all(g * x == x and x * g == x for x in G_els):
                e = g
                break
                
        for g in G_els:
            g_inv = None
            for x in G_els:
                if g * x == e and x * g == e:
                    g_inv = x
                    break
            for n in N_els:
                if g * n * g_inv not in N_els:
                    return False
                    
        return True
    except Exception:
        return False

def check_neg_Q(H, f, N):
    try:
        H_els = get_elements(H)
        N_els = get_elements(N)
        
        if callable(f):
            f_N = []
            for n in N_els:
                val = f(n)
                if val not in f_N:
                    f_N.append(val)
        else:
            f_N = []
            for n in N_els:
                val = f[n]
                if val not in f_N:
                    f_N.append(val)
                    
        if not is_group(H_els):
            return True
            
        if not is_group(f_N):
            return True
            
        e = None
        for h in H_els:
            if all(h * x == x and x * h == x for x in H_els):
                e = h
                break
                
        is_normal = True
        for h in H_els:
            h_inv = None
            for x in H_els:
                if h * x == e and x * h == e:
                    h_inv = x
                    break
            for y in f_N:
                if h * y * h_inv not in f_N:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        return not is_normal
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            N = witness.get('N')
        elif isinstance(witness, tuple) and len(witness) == 4:
            G, H, f, N = witness
        else:
            return [False, False, False]
            
        h1 = check_H1(G, H, f)
        h2 = check_H2(G, N)
        neg_q = check_neg_Q(H, f, N)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "H_2: N is a normal subgroup of G",
    "¬Q: The image f(N) is not a normal subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2