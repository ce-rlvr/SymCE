import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            h1 = False
        else:
            A, B = witness
            if hasattr(A, 'elements') and hasattr(B, 'elements') and \
               hasattr(A, 'generators') and hasattr(B, 'generators') and \
               hasattr(A, 'identity') and hasattr(B, 'identity'):
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            A, B = witness
            elements_A = list(A.elements)
            elements_B = list(B.elements)
            
            idx_A = {x: i for i, x in enumerate(elements_A)}
            idx_B = {x: i for i, x in enumerate(elements_B)}
            
            mul_A = [[idx_A[x * y] for y in elements_A] for x in elements_A]
            mul_B = [[idx_B[x * y] for y in elements_B] for x in elements_B]
            
            gens_A_idx = [idx_A[g] for g in A.generators]
            
            homs = []
            for img_idx in itertools.product(range(len(elements_B)), repeat=len(gens_A_idx)):
                f = {idx_A[A.identity]: idx_B[B.identity]}
                for g, i in zip(gens_A_idx, img_idx):
                    f[g] = i
                    
                queue = list(f.keys())
                head = 0
                valid = True
                while head < len(queue):
                    x = queue[head]
                    head += 1
                    for y in list(f.keys()):
                        xy = mul_A[x][y]
                        fx_fy = mul_B[f[x]][f[y]]
                        if xy in f:
                            if f[xy] != fx_fy:
                                valid = False
                                break
                        else:
                            f[xy] = fx_fy
                            queue.append(xy)
                        
                        yx = mul_A[y][x]
                        fy_fx = mul_B[f[y]][f[x]]
                        if yx in f:
                            if f[yx] != fy_fx:
                                valid = False
                                break
                        else:
                            f[yx] = fy_fx
                            queue.append(yx)
                    if not valid:
                        break
                        
                if valid and len(f) == len(elements_A):
                    all_valid = True
                    for x in range(len(elements_A)):
                        for y in range(len(elements_A)):
                            if f[mul_A[x][y]] != mul_B[f[x]][f[y]]:
                                all_valid = False
                                break
                        if not all_valid:
                            break
                    if all_valid:
                        homs.append(tuple(f[i] for i in range(len(elements_A))))
                        
            homs_set = set(homs)
            is_abelian_group = True
            
            for f in homs:
                for g in homs:
                    h = tuple(mul_B[f[i]][g[i]] for i in range(len(f)))
                    if h not in homs_set:
                        is_abelian_group = False
                        break
                    h_rev = tuple(mul_B[g[i]][f[i]] for i in range(len(f)))
                    if h != h_rev:
                        is_abelian_group = False
                        break
                if not is_abelian_group:
                    break
                    
            if is_abelian_group:
                identity = None
                for e in homs:
                    is_id = True
                    for f in homs:
                        ef = tuple(mul_B[e[i]][f[i]] for i in range(len(f)))
                        fe = tuple(mul_B[f[i]][e[i]] for i in range(len(f)))
                        if ef != f or fe != f:
                            is_id = False
                            break
                    if is_id:
                        identity = e
                        break
                if identity is None:
                    is_abelian_group = False
                else:
                    for f in homs:
                        has_inv = False
                        for g in homs:
                            fg = tuple(mul_B[f[i]][g[i]] for i in range(len(f)))
                            gf = tuple(mul_B[g[i]][f[i]] for i in range(len(f)))
                            if fg == identity and gf == identity:
                                has_inv = True
                                break
                        if not has_inv:
                            is_abelian_group = False
                            break
                            
            neg_q = not is_abelian_group
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "¬Q: Hom(A, B) does not form an abelian group under pointwise addition"
]
N_HYP = 1
NEG_Q_INDEX = 1