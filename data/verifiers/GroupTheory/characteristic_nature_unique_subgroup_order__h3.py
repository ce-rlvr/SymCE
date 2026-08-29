import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            if not G.is_normal(H):
                neg_q = True
            elif G.order() > 1:
                elems = list(G.generate())
                gens = G.generators
                order = G.order()
                
                for img in itertools.product(elems, repeat=len(gens)):
                    if PermutationGroup(*img).order() != order:
                        continue
                    
                    mapping = {G.identity: G.identity}
                    queue = [G.identity]
                    is_homo = True
                    
                    head = 0
                    while head < len(queue):
                        curr = queue[head]
                        head += 1
                        curr_img = mapping[curr]
                        
                        for i, g in enumerate(gens):
                            nxt = curr * g
                            nxt_img = curr_img * img[i]
                            if nxt in mapping:
                                if mapping[nxt] != nxt_img:
                                    is_homo = False
                                    break
                            else:
                                mapping[nxt] = nxt_img
                                queue.append(nxt)
                        if not is_homo:
                            break
                            
                    if is_homo:
                        preserves = True
                        for h in H.generators:
                            if not H.contains(mapping[h]):
                                preserves = False
                                break
                        if not preserves:
                            neg_q = True
                            break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2