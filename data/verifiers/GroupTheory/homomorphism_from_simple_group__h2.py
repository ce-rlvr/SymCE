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
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1 = False
        
    # H_2: f is a group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            
            if isinstance(f, dict):
                f_func = lambda x: f[x]
                if set(f.keys()) != set(G_elems):
                    h2 = False
                else:
                    h2 = True
            elif isinstance(f, (list, tuple)):
                f_dict = dict(f)
                f_func = lambda x: f_dict[x]
                if set(f_dict.keys()) != set(G_elems):
                    h2 = False
                else:
                    h2 = True
            else:
                f_func = f
                h2 = True
                
            if h2:
                for x in G_elems:
                    fx = f_func(x)
                    if fx not in H_elems:
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
        
    # neg_Q: f is neither injective nor trivial
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            G_elems = list(G.elements)
            H_id = H.identity
            
            is_trivial = True
            for x in G_elems:
                if f_func(x) != H_id:
                    is_trivial = False
                    break
                    
            is_injective = True
            G_id = G.identity
            for x in G_elems:
                if x != G_id and f_func(x) == H_id:
                    is_injective = False
                    break
                    
            neg_q = (not is_trivial) and (not is_injective)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: f is neither an injective homomorphism nor the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2