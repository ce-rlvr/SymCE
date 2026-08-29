import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
        G, H, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: f is a surjective group homomorphism
    try:
        if not h1:
            h2 = False
        else:
            order = G.order()
            if order > 2000:
                h2 = False
            else:
                G_els = list(G.generate())
                H_els = set(H.generate())
                
                is_hom = True
                images = set()
                
                for x in G_els:
                    if isinstance(f, dict):
                        fx = f.get(x)
                        if fx is None:
                            is_hom = False
                            break
                    else:
                        fx = f(x)
                    
                    if fx not in H_els:
                        is_hom = False
                        break
                    images.add(fx)
                    
                if is_hom:
                    for x in G_els:
                        if isinstance(f, dict):
                            fx = f.get(x)
                        else:
                            fx = f(x)
                        for y in G_els:
                            xy = x * y
                            if isinstance(f, dict):
                                fxy = f.get(xy)
                                fy = f.get(y)
                            else:
                                fxy = f(xy)
                                fy = f(y)
                            if fxy != fx * fy:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                
                is_surj = (images == H_els)
                h2 = is_hom and is_surj
    except Exception:
        h2 = False

    # neg_Q: H is not solvable
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not H.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a surjective group homomorphism",
    "¬Q: H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2