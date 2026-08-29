import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group, max_size=2000):
    if hasattr(group, 'elements'):
        try:
            return list(group.elements)
        except Exception:
            pass
    elements = []
    for i, g in enumerate(group.generate()):
        if i >= max_size:
            raise ValueError("Group too large")
        elements.append(g)
    return elements

def conditions(witness):
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False]
        
    def get_map(func, x):
        if isinstance(func, dict):
            return func[x]
        elif isinstance(func, list):
            for k, v in func:
                if k == x:
                    return v
            raise ValueError("Mapping not found")
        return func(x)

    # H1: G and H are groups
    try:
        h1 = hasattr(G, 'generate') and hasattr(H, 'generate') and hasattr(G, 'center') and hasattr(H, 'center')
    except Exception:
        h1 = False

    # H2: f is a surjective group homomorphism
    try:
        if not h1:
            h2 = False
        else:
            elements_G = get_elements(G)
            elements_H = get_elements(H)
            
            image = set()
            is_homo = True
            for g1 in elements_G:
                fg1 = get_map(f, g1)
                image.add(fg1)
                if fg1 not in elements_H:
                    is_homo = False
                    break
                for g2 in elements_G:
                    fg2 = get_map(f, g2)
                    fg1g2 = get_map(f, g1 * g2)
                    if fg1g2 != fg1 * fg2:
                        is_homo = False
                        break
                if not is_homo:
                    break
            
            is_surj = (len(image) == len(elements_H)) and all(h in image for h in elements_H)
            h2 = is_homo and is_surj
    except Exception:
        h2 = False

    # neg_Q: f(Z(G)) is NOT a subgroup of Z(H)
    try:
        if not h1:
            neg_q = False
        else:
            Z_G_elements = get_elements(G.center())
            
            f_ZG = set()
            for z in Z_G_elements:
                f_ZG.add(get_map(f, z))
                
            Z_H_elements = set(get_elements(H.center()))
            
            is_subgroup = True
            if not f_ZG:
                is_subgroup = False
            else:
                for x in f_ZG:
                    for y in f_ZG:
                        if x * y not in f_ZG:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                if is_subgroup:
                    for x in f_ZG:
                        if x**-1 not in f_ZG:
                            is_subgroup = False
                            break
                            
            is_subgroup_of_center = is_subgroup and f_ZG.issubset(Z_H_elements)
            neg_q = not is_subgroup_of_center
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a surjective group homomorphism",
    "¬Q: The image f(Z(G)) is not a subgroup of the center of H"
]

N_HYP = 2
NEG_Q_INDEX = 2