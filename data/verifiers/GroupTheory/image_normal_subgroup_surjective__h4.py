import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        f = witness.get('f')
        N = witness.get('N')
    else:
        try:
            G, H, f, N = witness
        except Exception:
            return [False, False, False, False]

    # H_1: G and H are groups and N is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            G_elements = set(G.elements)
            if isinstance(N, PermutationGroup):
                N_elements = set(N.elements)
            else:
                N_elements = set(N)
            
            if not N_elements.issubset(G_elements):
                h1 = False
            else:
                G_id = None
                for e in G_elements:
                    if e * e == e:
                        G_id = e
                        break
                
                if G_id not in N_elements:
                    h1 = False
                else:
                    for a in N_elements:
                        for b in N_elements:
                            if a * b not in N_elements:
                                h1 = False
                                break
                        if not h1:
                            break
    except Exception:
        h1 = False

    # H_2: f is a group homomorphism from G to H
    try:
        h2 = True
        G_elements = list(G.elements)
        H_elements = set(H.elements)
        if isinstance(f, dict):
            def f_eval(x): return f.get(x, None)
        else:
            f_eval = f
            
        for g in G_elements:
            if f_eval(g) not in H_elements:
                h2 = False
                break
        if h2:
            for a in G_elements:
                for b in G_elements:
                    if f_eval(a * b) != f_eval(a) * f_eval(b):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: f is surjective
    try:
        H_elements = set(H.elements)
        if isinstance(f, dict):
            def f_eval(x): return f.get(x, None)
        else:
            f_eval = f
        
        image = set(f_eval(g) for g in list(G.elements))
        h3 = (image == H_elements)
    except Exception:
        h3 = False

    # neg_Q: f(N) is not a normal subgroup of H
    try:
        if isinstance(f, dict):
            def f_eval(x): return f.get(x, None)
        else:
            f_eval = f
            
        if isinstance(N, PermutationGroup):
            N_elements = set(N.elements)
        else:
            N_elements = set(N)
            
        f_N = set(f_eval(n) for n in N_elements)
        H_elements = list(H.elements)
        
        H_id = None
        for e in H_elements:
            if e * e == e:
                H_id = e
                break
        
        is_normal = True
        if H_id not in f_N:
            is_normal = False
        else:
            for a in f_N:
                for b in f_N:
                    if a * b not in f_N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if is_normal:
                for h in H_elements:
                    h_inv = ~h
                    for n in f_N:
                        if h * n * h_inv not in f_N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and N is a subgroup of G",
    "H_2: f is a group homomorphism from G to H",
    "H_3: f is surjective",
    "¬Q: f(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3