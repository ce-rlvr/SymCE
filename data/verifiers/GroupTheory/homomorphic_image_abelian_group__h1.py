import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import math
import itertools
import functools

SymmetricGroup = sympy.combinatorics.named_groups.SymmetricGroup
AlternatingGroup = sympy.combinatorics.named_groups.AlternatingGroup
DihedralGroup = sympy.combinatorics.named_groups.DihedralGroup
CyclicGroup = sympy.combinatorics.named_groups.CyclicGroup
Permutation = sympy.combinatorics.permutations.Permutation
PermutationGroup = sympy.combinatorics.PermutationGroup
eye = sympy.matrices.eye
zeros = sympy.matrices.zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if hasattr(witness, "domain") and hasattr(witness, "codomain"):
            G = witness.domain
            H = witness.codomain
            f = witness
        else:
            G, H, f = witness
    except Exception:
        return [False, False, False]
        
    def get_f_val(x):
        if isinstance(f, dict):
            return f.get(x, None)
        elif isinstance(f, (list, tuple)):
            for k, v in f:
                if k == x:
                    return v
            return None
        return f(x)

    # H_1: f: G \to H is a group homomorphism
    h1_ok = False
    try:
        G_elems = list(G.elements)
        H_elems = set(H.elements)
        
        is_hom = True
        for x in G_elems:
            fx = get_f_val(x)
            if fx not in H_elems:
                is_hom = False
                break
                
        if is_hom:
            for x in G_elems:
                for y in G_elems:
                    if get_f_val(x * y) != get_f_val(x) * get_f_val(y):
                        is_hom = False
                        break
                if not is_hom:
                    break
        h1_ok = is_hom
    except Exception:
        h1_ok = False

    # H_2: G is an abelian group
    h2_ok = False
    try:
        h2_ok = bool(G.is_abelian)
    except Exception:
        h2_ok = False

    # ¬Q: The image f(G) is NOT an abelian subgroup of H
    neg_q_ok = False
    try:
        G_elems = list(G.elements)
        image = set()
        for x in G_elems:
            val = get_f_val(x)
            if val is not None:
                image.add(val)
        
        is_subgroup = True
        if not image:
            is_subgroup = False
        else:
            elem = next(iter(image))
            identity = elem * elem**-1
            if identity not in image:
                is_subgroup = False
            else:
                for a in image:
                    if a**-1 not in image:
                        is_subgroup = False
                        break
                    for b in image:
                        if a * b not in image:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
        is_abelian = True
        for a in image:
            for b in image:
                if a * b != b * a:
                    is_abelian = False
                    break
            if not is_abelian:
                break
                
        neg_q_ok = not (is_subgroup and is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: G is an abelian group",
    "¬Q: f(G) is not an abelian subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2