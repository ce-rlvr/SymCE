import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G_raw = witness['G']
        v = witness['v']
        w = witness['w']
    except (TypeError, KeyError):
        return [False, False, False]
        
    # H_1: G acts on the tensor product V ⊗ W via g · (v ⊗ w) = (g · v) ⊗ (g · w)
    try:
        h1 = True
        if not G_raw:
            h1 = False
        else:
            dim_v = v.rows
            dim_w = w.rows
            if v.cols != 1 or w.cols != 1:
                h1 = False
            
            G = []
            for g in G_raw:
                if isinstance(g, (tuple, list)) and len(g) == 2:
                    G.append(tuple(g))
                else:
                    G.append((g, g))
                    
            G_set = set()
            for A, B in G:
                if not isinstance(A, Matrix) or not isinstance(B, Matrix):
                    h1 = False
                    break
                if A.rows != dim_v or A.cols != dim_v:
                    h1 = False
                    break
                if B.rows != dim_w or B.cols != dim_w:
                    h1 = False
                    break
                G_set.add((tuple(A), tuple(B)))
                
            if h1:
                # Check closure under multiplication to ensure G is a valid group action
                for A1, B1 in G:
                    for A2, B2 in G:
                        A3 = A1 * A2
                        B3 = B1 * B2
                        if (tuple(A3), tuple(B3)) not in G_set:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: v ∈ V and w ∈ W
    try:
        h2 = isinstance(v, Matrix) and isinstance(w, Matrix)
    except Exception:
        h2 = False

    # ¬Q: The intersection of the individual point stabilizers Stab_G(v) ∩ Stab_G(w) 
    # is NOT a subgroup of the point stabilizer Stab_G(v ⊗ w)
    try:
        def tensor_product(a, b):
            return Matrix([ai * bj for ai in a for bj in b])
            
        vw = tensor_product(v, w)
        
        stab_v = []
        stab_w = []
        stab_vw = []
        
        for A, B in G:
            if A * v == v:
                stab_v.append((A, B))
            if B * w == w:
                stab_w.append((A, B))
            if tensor_product(A * v, B * w) == vw:
                stab_vw.append((A, B))
                
        intersection = [g for g in stab_v if g in stab_w]
        
        is_subgroup = all(g in stab_vw for g in intersection)
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G acts on the tensor product V ⊗ W via g · (v ⊗ w) = (g · v) ⊗ (g · w)",
    "H_2: v ∈ V and w ∈ W",
    "¬Q: Stab_G(v) ∩ Stab_G(w) is not a subgroup of Stab_G(v ⊗ w)"
]

N_HYP = 2
NEG_Q_INDEX = 2