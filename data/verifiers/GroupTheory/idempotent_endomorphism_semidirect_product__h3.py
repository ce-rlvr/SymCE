import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS: list[str] = [
    "H_1: G is a group",
    "H_2: f is a group endomorphism",
    "¬Q: G is not the internal semidirect product of ker(f) and im(f)"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2

def conditions(witness) -> list[bool]:
    try:
        G, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    f_map = {}
    elements = []
    elements_set = set()
    valid_map = False
    try:
        if h1:
            elements = list(G.generate())
            elements_set = set(elements)
            valid_map = True
            for g in elements:
                if callable(f):
                    fg = f(g)
                elif isinstance(f, dict):
                    fg = f[g]
                else:
                    valid_map = False
                    break
                if fg not in elements_set:
                    valid_map = False
                    break
                f_map[g] = fg
    except Exception:
        valid_map = False

    try:
        h2 = False
        if h1 and valid_map:
            h2 = True
            for x in elements:
                for y in elements:
                    if f_map[x * y] != f_map[x] * f_map[y]:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if h1 and valid_map:
            id_elem = G.identity
            ker_f = set(g for g in elements if f_map[g] == id_elem)
            im_f = set(f_map.values())
            
            is_sdp = True
            
            if id_elem not in ker_f or id_elem not in im_f:
                is_sdp = False
                
            if is_sdp:
                for x in ker_f:
                    for y in ker_f:
                        if (x * y) not in ker_f:
                            is_sdp = False
                            break
                    if not is_sdp: break
                    
            if is_sdp:
                for x in im_f:
                    for y in im_f:
                        if (x * y) not in im_f:
                            is_sdp = False
                            break
                    if not is_sdp: break
                    
            if is_sdp:
                for n in ker_f:
                    for g in elements:
                        if (g * n * ~g) not in ker_f:
                            is_sdp = False
                            break
                    if not is_sdp: break
                    
            if is_sdp:
                intersection = ker_f.intersection(im_f)
                product_set = set(n * h for n in ker_f for h in im_f)
                if intersection != {id_elem} or product_set != elements_set:
                    is_sdp = False
                    
            neg_q = not is_sdp
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]