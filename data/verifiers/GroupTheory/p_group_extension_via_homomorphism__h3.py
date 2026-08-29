import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

# Top-level setup
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

def is_p_group(n):
    if n <= 0:
        return False
    if n == 1:
        return True
    factors = factorint(n)
    return len(factors) == 1

def eval_f(f, x):
    if isinstance(f, dict):
        return f.get(x, None)
    elif isinstance(f, (list, tuple)):
        for k, v in f:
            if k == x:
                return v
        return None
    return f(x)

def conditions(witness):
    try:
        G, H, f = witness
    except Exception:
        return [False] * 5
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: f is a group homomorphism
    try:
        h2 = True
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        for g in G_elems:
            val = eval_f(f, g)
            if val not in H_elems:
                h2 = False
                break
        if h2:
            for g1 in G_elems:
                for g2 in G_elems:
                    val1 = eval_f(f, g1)
                    val2 = eval_f(f, g2)
                    val12 = eval_f(f, g1 * g2)
                    if val1 is None or val2 is None or val12 is None:
                        h2 = False
                        break
                    if val12 != val1 * val2:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # H_3: The kernel of f is a finite p-group
    try:
        H_elems = list(H.elements)
        id_H = None
        for h in H_elems:
            if h * h == h:
                id_H = h
                break
        ker_size = 0
        for g in list(G.elements):
            if eval_f(f, g) == id_H:
                ker_size += 1
        h3 = is_p_group(ker_size)
    except Exception:
        h3 = False
        
    # H_4: The image f(G) is a finite p-group
    try:
        im_elements = set()
        for g in list(G.elements):
            val = eval_f(f, g)
            if val is not None:
                im_elements.add(val)
        im_size = len(im_elements)
        h4 = is_p_group(im_size)
    except Exception:
        h4 = False
        
    # neg_Q: G is NOT a finite p-group
    try:
        neg_q = not is_p_group(G.order())
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "H_3: The kernel of f is a finite p-group",
    "H_4: The image f(G) is a finite p-group",
    "¬Q: G is not a finite p-group"
]

N_HYP = 4
NEG_Q_INDEX = 4