import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def get_all_homomorphisms(A, B):
    A_list = list(A.elements)
    B_list = list(B.elements)
    gens = A.generators
    id_A = A.identity
    id_B = B.identity
    
    valid_homs = []
    for target in itertools.product(B_list, repeat=len(gens)):
        mapping = {id_A: id_B}
        possible = True
        for g, t in zip(gens, target):
            if g == id_A and t != id_B:
                possible = False
                break
            mapping[g] = t
            
        if not possible:
            continue
            
        queue = list(mapping.keys())
        while queue:
            x = queue.pop(0)
            for g in gens:
                y = x * g
                val = mapping[x] * mapping[g]
                if y in mapping:
                    if mapping[y] != val:
                        possible = False
                        break
                else:
                    mapping[y] = val
                    queue.append(y)
            if not possible:
                break
        
        if possible and len(mapping) == len(A_list):
            is_hom = True
            for x in A_list:
                for y in A_list:
                    if mapping[x*y] != mapping[x]*mapping[y]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                hom_tuple = tuple(mapping[x] for x in A_list)
                if hom_tuple not in valid_homs:
                    valid_homs.append(hom_tuple)
    return valid_homs, A_list

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
    except Exception:
        return [False, False, False]
        
    # H_1: A and B are abelian groups
    try:
        h1 = bool(A.is_abelian and B.is_abelian)
    except Exception:
        h1 = False
        
    # H_2: Addition of homomorphisms is defined pointwise
    # This is a definitional hypothesis, so it holds by definition in our evaluation context.
    h2 = True
    
    # ¬Q: Hom(A, B) does NOT form an abelian group under pointwise addition
    try:
        homs, A_list = get_all_homomorphisms(A, B)
        
        is_group = True
        is_abelian = True
        
        # 1. Closure and Abelian check
        for f in homs:
            for g in homs:
                # Pointwise addition (multiplication in SymPy's PermutationGroup)
                fg = tuple(f[i] * g[i] for i in range(len(A_list)))
                if fg not in homs:
                    is_group = False
                    break
                gf = tuple(g[i] * f[i] for i in range(len(A_list)))
                if fg != gf:
                    is_abelian = False
            if not is_group:
                break
                
        # 2. Identity
        if is_group:
            has_id = False
            for e in homs:
                is_id = True
                for f in homs:
                    ef = tuple(e[i] * f[i] for i in range(len(A_list)))
                    fe = tuple(f[i] * e[i] for i in range(len(A_list)))
                    if ef != f or fe != f:
                        is_id = False
                        break
                if is_id:
                    has_id = True
                    break
            if not has_id:
                is_group = False
                
        # 3. Inverses
        if is_group and has_id:
            id_B = B.identity
            e_expected = tuple(id_B for _ in A_list)
            for f in homs:
                has_inv = False
                for g in homs:
                    fg = tuple(f[i] * g[i] for i in range(len(A_list)))
                    gf = tuple(g[i] * f[i] for i in range(len(A_list)))
                    if fg == e_expected and gf == e_expected:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
                    
        neg_q = not (is_group and is_abelian)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are abelian groups",
    "H_2: Addition of homomorphisms is defined pointwise",
    "¬Q: Hom(A, B) does not form an abelian group under pointwise addition"
]

N_HYP = 2
NEG_Q_INDEX = 2