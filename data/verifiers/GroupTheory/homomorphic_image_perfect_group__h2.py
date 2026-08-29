import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    try:
        G, H, f = witness
    except Exception:
        return [False, False]
        
    # H_1: f is a surjective group homomorphism from G to H
    try:
        G_elements = list(G.generate())
        H_elements = list(H.generate())
        
        def eval_f(x):
            if isinstance(f, dict):
                if x in f:
                    return f[x]
                for k, v in f.items():
                    if k == x:
                        return v
            elif isinstance(f, list):
                for k, v in f:
                    if k == x:
                        return v
            else:
                return f(x)
            raise KeyError(f"Element {x} not found in mapping")
            
        images = []
        h1_ok = True
        for x in G_elements:
            fx = eval_f(x)
            found = False
            for h in H_elements:
                if fx == h:
                    found = True
                    break
            if not found:
                h1_ok = False
                break
            images.append(fx)
            
        if h1_ok:
            unique_images = []
            for img in images:
                if not any(img == u for u in unique_images):
                    unique_images.append(img)
            if len(unique_images) != len(H_elements):
                h1_ok = False
                
        if h1_ok:
            for x in G_elements:
                for y in G_elements:
                    if eval_f(x * y) != eval_f(x) * eval_f(y):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False
        
    # neg_Q: H is not a perfect group
    try:
        D = H.derived_subgroup()
        neg_q = D.order() != H.order()
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "¬Q: H is not a perfect group"
]

N_HYP = 1
NEG_Q_INDEX = 1