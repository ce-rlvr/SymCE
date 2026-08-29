import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
from sympy import Matrix, eye, zeros, Symbol

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A and B are subgroups of G",
    "H_2: alpha is a group isomorphism from A to B",
    "H_3: t is a new generator symbol not contained in X",
    "¬Q: The presentation is not isomorphic to the HNN extension"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        A = witness['A']
        B = witness['B']
        alpha = witness['alpha']
        X = witness['X']
        R = witness['R']
        t = witness['t']
    except KeyError:
        return [False, False, False, False]

    def is_subgroup(elements, group):
        if not elements: 
            return False
        try:
            for e in elements:
                if e not in group:
                    return False
            for e1 in elements:
                for e2 in elements:
                    if e1 * e2 not in elements:
                        return False
            for e in elements:
                if e**-1 not in elements:
                    return False
            return True
        except Exception:
            return False

    try:
        if hasattr(A, 'elements'):
            A_elems = list(A.elements)
        else:
            A_elems = list(A)
    except Exception:
        A_elems = []

    try:
        if hasattr(B, 'elements'):
            B_elems = list(B.elements)
        else:
            B_elems = list(B)
    except Exception:
        B_elems = []

    try:
        h1 = is_subgroup(A_elems, G) and is_subgroup(B_elems, G)
    except Exception:
        h1 = False

    def is_iso(A_elems, B_elems, alpha_map):
        try:
            if len(alpha_map) != len(A_elems): 
                return False
            for a in A_elems:
                if a not in alpha_map: 
                    return False
                if alpha_map[a] not in B_elems: 
                    return False
            
            if len(set(alpha_map.values())) != len(B_elems): 
                return False
            
            for x in A_elems:
                for y in A_elems:
                    if alpha_map[x * y] != alpha_map[x] * alpha_map[y]:
                        return False
            return True
        except Exception:
            return False

    try:
        h2 = is_iso(A_elems, B_elems, alpha)
    except Exception:
        h2 = False

    try:
        h3 = t not in X
    except Exception:
        h3 = False

    try:
        neg_q = False
        A_words = witness.get('A_words')
        B_words = witness.get('B_words')
        
        if A_words is None or B_words is None:
            # If the witness does not provide a mapping from subgroup elements to words in X,
            # the presentation is ill-defined over X.
            neg_q = True
        else:
            rels = list(R)
            for a in A_elems:
                w_a = A_words.get(a)
                w_alpha_a = B_words.get(alpha[a])
                if w_a is None or w_alpha_a is None:
                    neg_q = True
                    break
                rel = t * w_a * t**-1 * w_alpha_a**-1
                rels.append(rel)
                
            if not neg_q:
                gens = list(X) + [t]
                gen_to_idx = {g: i for i, g in enumerate(gens)}
                matrix = []
                for r in rels:
                    row = [0] * len(gens)
                    for g, exp in r.array_form:
                        if g in gen_to_idx:
                            row[gen_to_idx[g]] += exp
                    matrix.append(row)
                
                if not matrix:
                    betti = len(gens)
                else:
                    M = Matrix(matrix)
                    betti = len(gens) - M.rank()
                
                is_finite = False
                if hasattr(G, 'is_finite') and G.is_finite:
                    is_finite = True
                elif hasattr(G, 'order'):
                    try:
                        if G.order() < float('inf'):
                            is_finite = True
                    except Exception:
                        pass
                elif hasattr(G, 'elements'):
                    is_finite = True
                elif isinstance(G, (list, set, tuple)):
                    is_finite = True
                    
                if is_finite:
                    # The HNN extension of a finite group has Betti number exactly 1.
                    # If the presentation has a different Betti number, it cannot be isomorphic.
                    if betti != 1:
                        neg_q = True
                    else:
                        neg_q = False
                else:
                    # For infinite groups, we conservatively return False if the presentation is well-formed.
                    neg_q = False
    except Exception:
        # Any type error or failure to construct the presentation means it is invalid.
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]