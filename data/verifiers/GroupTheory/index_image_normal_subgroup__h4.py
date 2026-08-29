import sympy
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism",
    "H_3: N is a normal subgroup of G",
    "not Q: The index of f(N) in H does not divide the index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_order(G):
    if hasattr(G, 'order'):
        o = G.order() if callable(G.order) else G.order
        return o
    if hasattr(G, 'elements'):
        return len(list(G.elements))
    return len(G)

def get_elements(G):
    if hasattr(G, 'order'):
        o = G.order() if callable(G.order) else G.order
        if o == sympy.oo:
            raise ValueError("Infinite group")
    if hasattr(G, 'elements'):
        return list(G.elements)
    return list(G)

def conditions(witness):
    try:
        G, H, f, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = (hasattr(G, 'is_group') or hasattr(G, 'elements')) and \
             (hasattr(H, 'is_group') or hasattr(H, 'elements'))
    except Exception:
        h1 = False
        
    # H_2: f is a surjective group homomorphism
    try:
        h2_ok = None
        if hasattr(f, 'is_surjective') and hasattr(f, 'is_homomorphism'):
            try:
                h2_ok = f.is_surjective() and f.is_homomorphism()
            except Exception:
                pass
                
        if h2_ok is None:
            G_els = get_elements(G)
            H_els = get_elements(H)
            
            if isinstance(f, dict):
                im = set(f.get(g, None) for g in G_els)
                is_hom = all(f.get(a*b, None) == f.get(a, None)*f.get(b, None) for a in G_els for b in G_els)
            else:
                im = set(f(g) for g in G_els)
                is_hom = all(f(a*b) == f(a)*f(b) for a in G_els for b in G_els)
                
            h2_ok = (set(H_els) == im) and is_hom
            
        h2 = bool(h2_ok)
    except Exception:
        h2 = False
        
    # H_3: N is a normal subgroup of G
    try:
        h3_ok = None
        if hasattr(G, 'is_normal'):
            try:
                h3_ok = G.is_normal(N)
            except Exception:
                pass
        if hasattr(N, 'is_normal') and h3_ok is None:
            try:
                if callable(N.is_normal):
                    h3_ok = N.is_normal(G)
                else:
                    h3_ok = N.is_normal
            except Exception:
                pass
                
        if h3_ok is None:
            N_els = set(get_elements(N))
            G_els = get_elements(G)
            h3_ok = True
            for g in G_els:
                inv_g = g**-1
                for n in N_els:
                    if g * n * inv_g not in N_els:
                        h3_ok = False
                        break
                if not h3_ok:
                    break
        h3 = bool(h3_ok)
    except Exception:
        h3 = False
        
    # neg_Q: The index of f(N) in H does not divide the index of N in G
    try:
        order_G = get_order(G)
        order_N = get_order(N)
        order_H = get_order(H)
        
        if order_G == sympy.oo or order_N == sympy.oo or order_H == sympy.oo:
            neg_q = True
        else:
            try:
                N_els = get_elements(N)
                if isinstance(f, dict):
                    f_N = set(f.get(n, None) for n in N_els)
                else:
                    f_N = set(f(n) for n in N_els)
                order_fN = len(f_N)
            except Exception:
                order_fN = get_order(f(N))
                
            index_G_N = int(order_G // order_N)
            index_H_fN = int(order_H // order_fN)
            
            neg_q = (index_G_N % index_H_fN != 0)
    except Exception:
        try:
            index_G_N = G.index(N)
            index_H_fN = H.index(f(N))
            if index_G_N == sympy.oo:
                neg_q = True
            else:
                neg_q = (index_G_N % index_H_fN != 0)
        except Exception:
            neg_q = False
            
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]