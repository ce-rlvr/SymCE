import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        G, H, A, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: A is a subgroup of G
    try:
        if isinstance(A, PermutationGroup):
            A_elems = set(A.generate())
        else:
            A_elems = set(A)
            
        G_elems = set(G.generate())
        
        if not A_elems.issubset(G_elems):
            h2 = False
        elif G.identity not in A_elems:
            h2 = False
        else:
            h2 = True
            for a in A_elems:
                if ~a not in A_elems:
                    h2 = False
                    break
                for b in A_elems:
                    if a * b not in A_elems:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # ¬Q: f^{-1}(f(A)) != A ker(f)
    try:
        if isinstance(A, PermutationGroup):
            A_elems = set(A.generate())
        else:
            A_elems = set(A)
            
        if isinstance(f, dict):
            def f_eval(x): return f[x]
        elif isinstance(f, (list, tuple)):
            f_dict = dict(f)
            def f_eval(x): return f_dict[x]
        else:
            f_eval = f
            
        G_elems = set(G.generate())
        H_elems = set(H.generate())
        
        for x in G_elems:
            if f_eval(x) not in H_elems:
                raise ValueError("f must map G to H")
                
        ker_f = {x for x in G_elems if f_eval(x) == H.identity}
        f_A = {f_eval(a) for a in A_elems}
        preimage = {x for x in G_elems if f_eval(x) in f_A}
        A_ker_f = {a * k for a in A_elems for k in ker_f}
        
        neg_q = preimage != A_ker_f
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A is a subgroup of G",
    "¬Q: f^{-1}(f(A)) != A ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2