import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    try:
        G, H, K, f = witness
    except Exception:
        return [False, False, False]

    f_dict = None
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'identity') and hasattr(H, 'identity')
        if h1:
            G_els = set(G.elements)
            H_els = set(H.elements)
            if callable(f):
                f_dict = {g: f(g) for g in G_els}
            elif isinstance(f, dict):
                f_dict = f
            else:
                h1 = False
                
            if h1 and f_dict is not None:
                if set(f_dict.keys()) != G_els:
                    h1 = False
                elif not all(v in H_els for v in f_dict.values()):
                    h1 = False
    except Exception:
        h1 = False

    try:
        h2 = False
        if hasattr(K, 'elements') and hasattr(K, 'identity') and hasattr(H, 'elements') and hasattr(H, 'identity'):
            K_els = set(K.elements)
            H_els = set(H.elements)
            if K_els.issubset(H_els) and K.identity == H.identity:
                closed = True
                for a in K_els:
                    for b in K_els:
                        if a * b not in K_els:
                            closed = False
                            break
                    if not closed:
                        break
                h2 = closed
    except Exception:
        h2 = False

    try:
        if f_dict is None or not hasattr(G, 'elements') or not hasattr(H, 'identity') or not hasattr(K, 'elements'):
            neg_q = False
        else:
            ker_f = {g for g in G.elements if f_dict[g] == H.identity}
            pre_K = {g for g in G.elements if f_dict[g] in K.elements}
            
            is_sub = True
            if G.identity not in pre_K:
                is_sub = False
            else:
                for a in pre_K:
                    for b in pre_K:
                        if a * b not in pre_K:
                            is_sub = False
                            break
                    if not is_sub:
                        break
                if is_sub:
                    for a in pre_K:
                        if a**-1 not in pre_K:
                            is_sub = False
                            break
            
            contains_ker = ker_f.issubset(pre_K)
            
            q = is_sub and contains_ker
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: K is a subgroup of H",
    "¬Q: f^{-1}(K) is not a subgroup of G or does not contain ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2