import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        f = witness['f']
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
    except Exception:
        f_func = None

    try:
        if not h1 or f_func is None:
            h2 = False
        else:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            h2 = True
            for g in G_elems:
                if f_func(g) not in H_elems:
                    h2 = False
                    break
            if h2:
                for x in G_elems:
                    for y in G_elems:
                        if f_func(x * y) != f_func(x) * f_func(y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    try:
        G = witness['G']
        N = witness['N']
        if not isinstance(N, PermutationGroup):
            h3 = False
        else:
            N_elems = list(N.elements)
            G_elems = list(G.elements)
            
            is_sub = True
            for n in N_elems:
                if n not in G_elems:
                    is_sub = False
                    break
            
            if not is_sub:
                h3 = False
            else:
                is_norm = True
                for g in G_elems:
                    g_inv = ~g
                    for n in N_elems:
                        if g * n * g_inv not in N_elems:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
    except Exception:
        h3 = False

    try:
        H = witness['H']
        N = witness['N']
        N_elems = list(N.elements)
        f_N_elems = []
        for n in N_elems:
            fn = f_func(n)
            if fn not in f_N_elems:
                f_N_elems.append(fn)
                
        H_elems = list(H.elements)
        
        is_subgroup = True
        if not f_N_elems:
            is_subgroup = False
        else:
            for x in f_N_elems:
                for y in f_N_elems:
                    if x * y not in f_N_elems:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                for x in f_N_elems:
                    if ~x not in f_N_elems:
                        is_subgroup = False
                        break
                        
        if not is_subgroup:
            is_normal = False
        else:
            is_normal = True
            for h in H_elems:
                h_inv = ~h
                for y in f_N_elems:
                    if h * y * h_inv not in f_N_elems:
                        is_normal = False
                        break
                if not is_normal:
                    break
        
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a group homomorphism from G to H",
    "H_3: N is a normal subgroup of G",
    "¬Q: f(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3