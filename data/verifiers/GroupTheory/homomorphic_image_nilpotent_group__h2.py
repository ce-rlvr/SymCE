import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: f: G -> H is a surjective group homomorphism
    h1_ok = False
    try:
        G, H, f = witness
        
        if isinstance(f, dict):
            f_eval = lambda x: f.get(x, None)
        elif callable(f):
            f_eval = f
        else:
            f_eval = None
            
        if f_eval is not None:
            G_elems = list(G.elements)
            H_elems = set(H.elements)
            
            image = set()
            valid_homomorphism = True
            for g in G_elems:
                img = f_eval(g)
                if img is None or img not in H_elems:
                    valid_homomorphism = False
                    break
                image.add(img)
                
            if valid_homomorphism and len(image) == len(H_elems):
                for g1 in G_elems:
                    for g2 in G_elems:
                        if f_eval(g1 * g2) != f_eval(g1) * f_eval(g2):
                            valid_homomorphism = False
                            break
                    if not valid_homomorphism:
                        break
                h1_ok = valid_homomorphism
    except Exception:
        h1_ok = False

    # neg_Q: H is not a nilpotent group
    neg_q_ok = False
    try:
        G, H, f = witness
        neg_q_ok = not bool(H.is_nilpotent)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "¬Q: H is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1