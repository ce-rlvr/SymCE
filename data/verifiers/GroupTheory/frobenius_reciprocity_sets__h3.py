import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, Y, action = witness
    except Exception:
        return [False, False, False]
        
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            h1 = False
        else:
            elements = list(G.generate())
            id_g = G.identity
            
            is_left = True
            try:
                for y in Y:
                    if action(id_g, y) != y:
                        is_left = False
                        break
                if is_left:
                    for g1 in elements:
                        for g2 in elements:
                            for y in Y:
                                if action(g1, action(g2, y)) != action(g1 * g2, y):
                                    is_left = False
                                    break
                            if not is_left: break
                        if not is_left: break
            except Exception:
                is_left = False
                
            is_right = True
            try:
                for y in Y:
                    if action(y, id_g) != y:
                        is_right = False
                        break
                if is_right:
                    for g1 in elements:
                        for g2 in elements:
                            for y in Y:
                                if action(action(y, g1), g2) != action(y, g1 * g2):
                                    is_right = False
                                    break
                            if not is_right: break
                        if not is_right: break
            except Exception:
                is_right = False
                
            h1 = is_left or is_right
    except Exception:
        h1 = False
        
    try:
        h2 = H.is_subgroup(G)
    except Exception:
        h2 = False
        
    try:
        if not h1 or not h2:
            return [h1, h2, False]
            
        H_elements = set(H.generate())
        cosets = []
        for g in elements:
            c = frozenset(g * h for h in H_elements)
            if c not in cosets:
                cosets.append(c)
                
        equivariant_maps = 0
        for y in Y:
            f = {}
            possible = True
            for g in elements:
                c = frozenset(g * h for h in H_elements)
                if is_left:
                    val = action(g, y)
                else:
                    val = action(y, g)
                if c in f and f[c] != val:
                    possible = False
                    break
                f[c] = val
            
            if not possible:
                continue
                
            equiv = True
            for g in elements:
                for c in cosets:
                    gc = frozenset(g * x for x in c)
                    if is_left:
                        expected = action(g, f[c])
                    else:
                        expected = action(f[c], g)
                    if f[gc] != expected:
                        equiv = False
                        break
                if not equiv:
                    break
            if equiv:
                equivariant_maps += 1
                
        fixed_points = 0
        for y in Y:
            is_fixed = True
            for h in H_elements:
                if is_left:
                    if action(h, y) != y:
                        is_fixed = False
                        break
                else:
                    if action(y, h) != y:
                        is_fixed = False
                        break
            if is_fixed:
                fixed_points += 1
                
        neg_q = (equivariant_maps != fixed_points)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set Y",
    "H_2: H is a subgroup of G",
    "¬Q: The number of G-equivariant maps from G/H to Y is not equal to the size of Y^H"
]

N_HYP = 2
NEG_Q_INDEX = 2